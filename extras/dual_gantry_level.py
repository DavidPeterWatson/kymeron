# Mechanical bed tilt calibration with multiple Z steppers
#
# Copyright (C) 2018-2019  Kevin O'Connor <kevin@koconnor.net>
#
# This file may be distributed under the terms of the GNU GPLv3 license.
import logging
import mathutil
from . import multi_axis_probe


class GantryAdjustHelper:
    def __init__(self, config, gantry_position_count, direction):
        self.printer = config.get_printer()
        self.name = config.get_name()
        self.gantry_position_count = gantry_position_count
        self.gantry_steppers = []
        (axis, sense) = multi_axis_probe.direction_types[direction]
        self.axis = axis
        self.axis_name = multi_axis_probe.axis_names[axis]
        self.printer.register_event_handler("klippy:connect", self.handle_connect)
    def handle_connect(self):
        kin = self.printer.lookup_object('toolhead').get_kinematics()
        gantry_steppers = [s for s in kin.get_steppers() if s.is_active_axis(self.axis_name)]
        if len(gantry_steppers) != self.gantry_position_count:
            raise self.printer.config_error(f"{self.name} gantry_positions needs exactly {len(gantry_steppers)} items")
        if len(gantry_steppers) < 2:
            raise self.printer.config_error(f"{self.name} requires multiple {self.axis_name} steppers")
        self.gantry_steppers = gantry_steppers
    def adjust_steppers(self, adjustments, speed):
        toolhead = self.printer.lookup_object('toolhead')
        gcode = self.printer.lookup_object('gcode')
        curpos = toolhead.get_position()
        # Report on movements
        stepstrs = ["%s = %.6f" % (s.get_name(), a)
                    for s, a in zip(self.gantry_steppers, adjustments)]
        msg = "Making the following stepper adjustments:\n%s" % ("\n".join(stepstrs),)
        gcode.respond_info(msg)
        # Disable stepper movements
        toolhead.flush_step_generation()
        for s in self.gantry_steppers:
            s.set_trapq(None)
        # Move each stepper (sorted from lowest to highest) until they match
        positions = [(-a, s) for a, s in zip(adjustments, self.gantry_steppers)]
        positions.sort(key=(lambda k: k[0]))
        first_stepper_offset, first_stepper = positions[0]
        low = curpos[self.axis] - first_stepper_offset
        for i in range(len(positions)-1):
            stepper_offset, stepper = positions[i]
            next_stepper_offset, next_stepper = positions[i+1]
            toolhead.flush_step_generation()
            stepper.set_trapq(toolhead.get_trapq())
            curpos[self.axis] = low + next_stepper_offset
            try:
                toolhead.move(curpos, speed)
                toolhead.set_position(curpos)
            except:
                logging.exception("GantryAdjustHelper adjust_steppers")
                toolhead.flush_step_generation()
                for s in self.gantry_steppers:
                    s.set_trapq(toolhead.get_trapq())
                raise
        # gantry should now be level - do final cleanup
        last_stepper_offset, last_stepper = positions[-1]
        toolhead.flush_step_generation()
        last_stepper.set_trapq(toolhead.get_trapq())
        curpos[self.axis] += first_stepper_offset
        toolhead.set_position(curpos)


class GantryAdjustStatus:
    def __init__(self, printer):
        self.applied = False
        printer.register_event_handler("stepper_enable:motor_off",
                                        self._motor_off)
    def check_retry_result(self, retry_result):
        if retry_result == "done":
            self.applied = True
        return retry_result
    def reset(self):
        self.applied = False
    def get_status(self, eventtime):
        return {'applied': self.applied}
    def _motor_off(self, print_time):
        self.reset()


class RetryHelper:
    def __init__(self, config, error_msg_extra = ""):
        self.gcode = config.get_printer().lookup_object('gcode')
        self.default_max_retries = config.getint("retries", 0, minval=0)
        self.default_retry_tolerance = \
            config.getfloat("retry_tolerance", 0., above=0.)
        self.value_label = "Probed points range"
        self.error_msg_extra = error_msg_extra
    def start(self, gcmd):
        self.max_retries = gcmd.get_int('RETRIES', self.default_max_retries,
                                        minval=0, maxval=30)
        self.retry_tolerance = gcmd.get_float('RETRY_TOLERANCE',
                                              self.default_retry_tolerance,
                                              minval=0.0, maxval=1.0)
        self.current_retry = 0
        self.previous = None
        self.increasing = 0
    def check_increase(self, error):
        if self.previous and error > self.previous + 0.0000001:
            self.increasing += 1
        elif self.increasing > 0:
            self.increasing -= 1
        self.previous = error
        return self.increasing > 1
    def check_retry(self, gantry_positions):
        if self.max_retries == 0:
            return "done"
        error = round(max(gantry_positions) - min(gantry_positions),6)
        self.gcode.respond_info(
            "Retries: %d/%d %s: %0.6f tolerance: %0.6f" % (
                self.current_retry, self.max_retries, self.value_label,
                error, self.retry_tolerance))
        if self.check_increase(error):
            raise self.gcode.error(f"Retries aborting: {self.value_label} is increasing. {self.error_msg_extra}")
        if error <= self.retry_tolerance:
            return "done"
        self.current_retry += 1
        if self.current_retry > self.max_retries:
            raise self.gcode.error("Too many retries")
        return "retry"


class DualGantryLevel:
    def __init__(self, config):
        self.printer = config.get_printer()
        self.name = config.get_name().split(' ')[-1]
        self.probe_direction = config.get('probe_direction')
        (axis, sense) = multi_axis_probe.direction_types[self.probe_direction]
        self.axis = axis
        self.gantry_positions = config.getlists('gantry_positions', seps=(',', '\n'), parser=float, count=2)
        self.retry_helper = RetryHelper(config)
        self.probe_helper = multi_axis_probe.ProbePointsHelper(config, self.probe_finalize)
        self.probe_helper.minimum_points(2)
        self.gantry_status = GantryAdjustStatus(self.printer)
        self.gantry_helper = GantryAdjustHelper(config, len(self.gantry_positions), self.probe_direction)
        # Register DUAL_GANTRY_LEVEL command
        gcode = self.printer.lookup_object('gcode')
        gcode.register_command(f'DUAL_GANTRY_LEVEL_{self.name}', self.cmd_DUAL_GANTRY_LEVEL, desc=self.cmd_DUAL_GANTRY_LEVEL_help)

    cmd_DUAL_GANTRY_LEVEL_help = "Adjust the gantry level"
    def cmd_DUAL_GANTRY_LEVEL(self, gcmd):
        self.gantry_status.reset()
        self.retry_helper.start(gcmd)
        self.probe_helper.start_probe(gcmd)

    def probe_finalize(self, positions):
        # Setup for coordinate descent analysis
        # x_offset = offsets[0]
        # y_offset = offsets[1]
        # z_offset = offsets[2]
        logging.info("Calculating gantry tilt with: %s", positions)
        return 'ok'
        # params = { 'x_adjust': x_offset, 'y_adjust': y_offset, 'z_adjust': z_offset }
        # Perform coordinate descent
        # def adjusted_height(pos):
        #     x, y, z = pos
        #     return (z - x - y)
        # def errorfunc(params):
        #     total_error = 0.
        #     for pos in positions:
        #         total_error += adjusted_height(pos, params)**2
        #     return total_error
        # new_params = mathutil.coordinate_descent(params.keys(), params, errorfunc)
        # # Apply results
        # speed = self.probe_helper.get_lift_speed()
        # logging.info("Calculated bed tilt parameters: %s", new_params)
        # x_adjust = 0
        # y_adjust = 0
        # z_adjust = (new_params['z_adjust'] - x_adjust  - y_adjust)
        # adjustments = [x*x_adjust + y*y_adjust + z_adjust for x, y in self.gantry_positions]
        # self.gantry_helper.adjust_steppers(adjustments, speed)
        # return self.gantry_status.check_retry_result(
        #     self.retry_helper.check_retry([p[self.axis] for p in positions]))

    def get_status(self, eventtime):
            return self.gantry_status.get_status(eventtime)


def load_config_prefix(config):
    return DualGantryLevel(config)
