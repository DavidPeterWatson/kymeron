# Z-Probe support
#
# Copyright (C) 2017-2024  Kevin O'Connor <kevin@koconnor.net>
#
# This file may be distributed under the terms of the GNU GPLv3 license.
import logging
from typing import List
import pins
from . import manual_probe
direction_types = {'x+': [0, +1], 'x-': [0, -1], 'y+': [1, +1], 'y-': [1, -1],
                   'z+': [2, +1], 'z-': [2, -1]}

HINT_TIMEOUT = """
If the probe did not move far enough to trigger, then
consider reducing the Z axis minimum position so the probe
can travel further (the Z minimum position can be negative).
"""

# Calculate the average Z from a set of positions
def calc_probe_z_average(positions, method='average'):
    if method != 'median':
        # Use mean average
        count = float(len(positions))
        return [sum([pos[i] for pos in positions]) / count
                for i in range(3)]
    # Use median
    z_sorted = sorted(positions, key=(lambda p: p[2]))
    middle = len(positions) // 2
    if (len(positions) & 1) == 1:
        # odd number of samples
        return z_sorted[middle]
    # even number of samples
    return calc_probe_z_average(z_sorted[middle-1:middle+1], 'average')


# Helper to read the xyz probe offsets from the config
class ProbeOffsetsHelper:
    def __init__(self, config):
        self.x_offset = config.getfloat('x_offset', 0.)
        self.y_offset = config.getfloat('y_offset', 0.)
        self.z_offset = config.getfloat('z_offset', 0.)
    def get_offsets(self):
        return self.x_offset, self.y_offset, self.z_offset


######################################################################
# Tools for utilizing the probe
######################################################################

# Helper code that can probe a series of points and report the
# position at each point.
class ProbePointsHelper:
    def __init__(self, config, finalize_callback, default_points=None):
        self.printer = config.get_printer()
        self.finalize_callback = finalize_callback
        self.probe_points = default_points
        self.name = config.get_name()
        self.gcode = self.printer.lookup_object('gcode')
        # Read config settings
        if default_points is None or config.get('points', None) is not None:
            self.probe_points = config.getlists('points', seps=(',', '\n'),
                                                parser=float, count=2)
        def_move_z = config.getfloat('horizontal_move_z', 5.)
        self.default_horizontal_move_z = def_move_z
        self.probe_speed = config.getfloat('probe_speed', 50., above=0.)
        self.use_offsets = False
        # Internal probing state
        self.lift_speed = self.probe_speed
        self.probe_offsets = (0., 0., 0.)
        self.manual_results = []
    def minimum_points(self,n):
        if len(self.probe_points) < n:
            raise self.printer.config_error(
                "Need at least %d probe points for %s" % (n, self.name))
    def update_probe_points(self, points, min_points):
        self.probe_points = points
        self.minimum_points(min_points)
    def use_xy_offsets(self, use_offsets):
        self.use_offsets = use_offsets
    def get_lift_speed(self):
        return self.lift_speed
    def _move(self, coord, probe_speed):
        self.printer.lookup_object('toolhead').manual_move(coord, probe_speed)
    def _raise_tool(self, is_first=False, direction='z-'):
        probe_speed = self.lift_speed
        if is_first:
            # Use full probe_speed to first probe position
            probe_speed = self.probe_speed
        self._move([None, None, self.horizontal_move_z], probe_speed)
    def _invoke_callback(self, results):
        # Flush lookahead queue
        toolhead = self.printer.lookup_object('toolhead')
        toolhead.get_last_move_time()
        # Invoke callback
        res = self.finalize_callback(self.probe_offsets, results)
        return res != "retry"
    def _move_next(self, probe_num):
        # Move to next XY probe point
        nextpos = list(self.probe_points[probe_num])
        if self.use_offsets:
            nextpos[0] -= self.probe_offsets[0]
            nextpos[1] -= self.probe_offsets[1]
        self._move(nextpos, self.probe_speed)
    def start_probe(self, gcmd, direction='z-'):
        manual_probe.verify_no_manual_probe(self.printer)
        # Lookup objects
        probe = self.printer.lookup_object('probe', None)
        method = gcmd.get('METHOD', 'automatic').lower()
        def_move_z = self.default_horizontal_move_z
        self.horizontal_move_z = gcmd.get_float('HORIZONTAL_MOVE_Z',
                                                def_move_z)
        if probe is None or method == 'manual':
            # Manual probe
            self.lift_speed = self.probe_speed
            self.probe_offsets = (0., 0., 0.)
            self.manual_results = []
            self._manual_probe_start()
            return
        # Perform automatic probing
        self.lift_speed = probe.get_probe_params(gcmd)['lift_speed']
        self.probe_offsets = probe.get_offsets()
        if self.horizontal_move_z < self.probe_offsets[2]:
            raise gcmd.error("horizontal_move_z can't be less than"
                             " probe's z_offset")
        probe_session = probe.start_probe_session(gcmd)
        probe_num = 0
        while 1:
            self._raise_tool(not probe_num)
            if probe_num >= len(self.probe_points):
                results = probe_session.pull_probed_results()
                done = self._invoke_callback(results)
                if done:
                    break
                # Caller wants a "retry" - restart probing
                probe_num = 0
            self._move_next(probe_num)
            probe_session.run_probe(gcmd, direction)
            probe_num += 1
        probe_session.end_probe_session()
    def _manual_probe_start(self):
        self._raise_tool(not self.manual_results)
        if len(self.manual_results) >= len(self.probe_points):
            done = self._invoke_callback(self.manual_results)
            if done:
                return
            # Caller wants a "retry" - clear results and restart probing
            self.manual_results = []
        self._move_next(len(self.manual_results))
        gcmd = self.gcode.create_gcode_command("", "", {})
        manual_probe.ManualProbeHelper(self.printer, gcmd,
                                       self._manual_probe_finalize)
    def _manual_probe_finalize(self, kin_pos):
        if kin_pos is None:
            return
        self.manual_results.append(kin_pos)
        self._manual_probe_start()

# Helper to obtain a single probe measurement
def run_single_probe(probe, gcmd, direction='z-'):
    probe_session = probe.start_probe_session(gcmd)
    probe_session.run_probe(gcmd)
    pos = probe_session.pull_probed_results()[0]
    probe_session.end_probe_session()
    return pos

class ProbeEndstopWrapper:
    def __init__(self, config, axis):
        self.printer = config.get_printer()
        self.axis = axis
        # Create an "endstop" object to handle the probe pin
        pins = self.printer.lookup_object('pins')
        pin = config.get('pin')
        pins.allow_multi_use_pin(pin.replace('^', '').replace('!', ''))
        pin_params = pins.lookup_pin(pin, can_invert=True, can_pullup=True)
        mcu = pin_params['chip']
        self.mcu_endstop = mcu.setup_pin('endstop', pin_params)
        self.printer.register_event_handler('klippy:mcu_identify', self._handle_mcu_identify)
        # Wrappers
        self.get_mcu = self.mcu_endstop.get_mcu
        self.add_stepper = self.mcu_endstop.add_stepper
        self.get_steppers = self._get_steppers
        self.home_start = self.mcu_endstop.home_start
        self.home_wait = self.mcu_endstop.home_wait
        self.query_endstop = self.mcu_endstop.query_endstop

    def _get_steppers(self):
        return self.mcu_endstop.get_steppers()

    def _handle_mcu_identify(self):
        kin = self.printer.lookup_object('toolhead').get_kinematics()
        for stepper in kin.get_steppers():
            if stepper.is_active_axis(self.axis):
                self.add_stepper(stepper)

    def get_position_endstop(self):
        return 0.

    def probing_move(self, pos, probe_speed):
        homing = self.printer.lookup_object('homing')
        return homing.probing_move(self, pos, probe_speed)



######################################################################
# Probe device implementation helpers
######################################################################

# Helper to implement common probing commands
class ProbeCommandHelper:
    def __init__(self, config, mcu_probes: List[ProbeEndstopWrapper]):
        self.printer = config.get_printer()
        self.mcu_probes = mcu_probes
        self.name = config.get_name()
        gcode = self.printer.lookup_object('gcode')

        # QUERY_PROBE command
        self.last_state = False
        gcode.register_command('QUERY_PROBE', self.cmd_QUERY_PROBE, desc=self.cmd_QUERY_PROBE_help)
        # PROBE command
        self.last_result = [0., 0., 0.]
        gcode.register_command('PROBE', self.cmd_PROBE,
                               desc=self.cmd_PROBE_help)
        # PROBE_CALIBRATE command
        self.probe_calibrate_z = 0.
        gcode.register_command('PROBE_CALIBRATE', self.cmd_PROBE_CALIBRATE,
                               desc=self.cmd_PROBE_CALIBRATE_help)
        # Other commands
        gcode.register_command('PROBE_ACCURACY', self.cmd_PROBE_ACCURACY,
                               desc=self.cmd_PROBE_ACCURACY_help)
        gcode.register_command('Z_OFFSET_APPLY_PROBE',
                               self.cmd_Z_OFFSET_APPLY_PROBE,
                               desc=self.cmd_Z_OFFSET_APPLY_PROBE_help)
        
    def _move(self, coord, probe_speed):
        self.printer.lookup_object('toolhead').manual_move(coord, probe_speed)

    def get_status(self, eventtime):
        return {'name': self.name,
                'last_query': self.last_state,
                'last_z_result': self.last_z_result}

    cmd_QUERY_PROBE_help = "Return the status of the z-probe"
    def cmd_QUERY_PROBE(self, gcmd, axis=2):
        query_endstop = self.mcu_probes[axis].query_endstop
        if query_endstop is None:
            raise gcmd.error("Probe does not support QUERY_PROBE")
        toolhead = self.printer.lookup_object('toolhead')
        print_time = toolhead.get_last_move_time()
        res = query_endstop(print_time)
        self.last_state = res
        gcmd.respond_info("probe: %s" % (["open", "TRIGGERED"][not not res],))

    cmd_PROBE_help = "Probe Z-height at current XY position"
    def cmd_PROBE(self, gcmd, axis=2):
        pos = run_single_probe(self.mcu_probes[axis], gcmd)
        gcmd.respond_info("Result is z=%.6f" % (pos[2],))
        self.last_z_result = pos[2]

    def probe_calibrate_finalize(self, kin_pos):
        if kin_pos is None:
            return
        z_offset = self.probe_calibrate_z - kin_pos[2]
        gcode = self.printer.lookup_object('gcode')
        gcode.respond_info(
            "%s: z_offset: %.3f\n"
            "The SAVE_CONFIG command will update the printer config file\n"
            "with the above and restart the printer." % (self.name, z_offset))
        configfile = self.printer.lookup_object('configfile')
        configfile.set(self.name, 'z_offset', "%.3f" % (z_offset,))

    cmd_PROBE_CALIBRATE_help = "Calibrate the probe's z_offset"
    def cmd_PROBE_CALIBRATE(self, gcmd, direction='z-'):
        manual_probe.verify_no_manual_probe(self.printer)
        (axis, sense) = direction_types[direction]
        probe = self.mcu_probes[axis]
        params = probe.get_probe_params(gcmd)
        # Perform initial probe
        curpos = run_single_probe(probe, gcmd)
        # Move away from the bed
        self.probe_calibrate_z = curpos[2]
        curpos[2] += 5.
        self._move(curpos, params['lift_speed'])
        # Move the nozzle over the probe point
        x_offset, y_offset, z_offset = probe.get_offsets()
        curpos[0] += x_offset
        curpos[1] += y_offset
        self._move(curpos, params['probe_speed'])
        # Start manual probe
        manual_probe.ManualProbeHelper(self.printer, gcmd,
                                       self.probe_calibrate_finalize)

    cmd_PROBE_ACCURACY_help = "Probe Z-height accuracy at current XY position"
    def cmd_PROBE_ACCURACY(self, gcmd, direction='z-'):
        (axis, sense) = direction_types[direction]
        probe = self.mcu_probes[axis]
        params = probe.get_probe_params(gcmd)
        sample_count = gcmd.get_int("SAMPLES", 10, minval=1)
        toolhead = self.printer.lookup_object('toolhead')
        pos = toolhead.get_position()
        gcmd.respond_info("PROBE_ACCURACY at X:%.3f Y:%.3f Z:%.3f"
                          " (samples=%d retract=%.3f"
                          " probe_speed=%.1f lift_speed=%.1f)\n"
                          % (pos[0], pos[1], pos[2],
                             sample_count, params['sample_retract_dist'],
                             params['probe_speed'], params['lift_speed']))
        # Create dummy gcmd with SAMPLES=1
        fo_params = dict(gcmd.get_command_parameters())
        fo_params['SAMPLES'] = '1'
        gcode = self.printer.lookup_object('gcode')
        fo_gcmd = gcode.create_gcode_command("", "", fo_params)
        # Probe bed sample_count times
        probe_session = probe.start_probe_session(fo_gcmd)
        probe_num = 0
        while probe_num < sample_count:
            # Probe position
            probe_session.run_probe(fo_gcmd)
            probe_num += 1
            # Retract
            pos = toolhead.get_position()
            liftpos = [None, None, pos[axis] + params['sample_retract_dist']]
            self._move(liftpos, params['lift_speed'])
        positions = probe_session.pull_probed_results()
        probe_session.end_probe_session()
        # Calculate maximum, minimum and average values
        max_value = max([p[axis] for p in positions])
        min_value = min([p[axis] for p in positions])
        range_value = max_value - min_value
        avg_value = calc_probe_z_average(positions, 'average')[2]
        median = calc_probe_z_average(positions, 'median')[2]
        # calculate the standard deviation
        deviation_sum = 0
        for i in range(len(positions)):
            deviation_sum += pow(positions[i][axis] - avg_value, 2.)
        sigma = (deviation_sum / len(positions)) ** 0.5
        # Show information
        gcmd.respond_info(
            "probe accuracy results: maximum %.6f, minimum %.6f, range %.6f, "
            "average %.6f, median %.6f, standard deviation %.6f" % (
            max_value, min_value, range_value, avg_value, median, sigma))

    cmd_Z_OFFSET_APPLY_PROBE_help = "Adjust the probe's z_offset"
    def cmd_Z_OFFSET_APPLY_PROBE(self, gcmd, direction='z-'):
        gcode_move = self.printer.lookup_object("gcode_move")
        offset = gcode_move.get_status()['homing_origin'].z
        (axis, sense) = direction_types[direction]
        probe = self.mcu_probes[axis]
        if offset == 0:
            gcmd.respond_info("Nothing to do: Z Offset is 0")
            return
        z_offset = probe.get_offsets()[axis]
        new_calibrate = z_offset - offset
        gcmd.respond_info(
            "%s: z_offset: %.3f\n"
            "The SAVE_CONFIG command will update the printer config file\n"
            "with the above and restart the printer."
            % (self.name, new_calibrate))
        configfile = self.printer.lookup_object('configfile')
        configfile.set(self.name, 'z_offset', "%.3f" % (new_calibrate,))


# Helper to track multiple probe attempts in a single command
class ProbeSessionHelper:
    def __init__(self, config, mcu_probes: List[ProbeEndstopWrapper]):
        self.printer = config.get_printer()
        self.mcu_probes = mcu_probes
        gcode = self.printer.lookup_object('gcode')
        self.dummy_gcode_cmd = gcode.create_gcode_command("", "", {})
        # Infer Z position to move to during a probe
        if config.has_section('stepper_z'):
            zconfig = config.getsection('stepper_z')
            self.z_position = zconfig.getfloat('position_min', 0.,
                                               note_valid=False)
        else:
            pconfig = config.getsection('printer')
            self.z_position = pconfig.getfloat('minimum_z_position', 0.,
                                               note_valid=False)
        # Configurable probing speeds
        self.probe_speed = config.getfloat('probe_speed', 5.0, above=0.)
        self.travel_speed = config.getfloat('travel_speed', 10.0, above=0.)

        # Multi-sample support (for improved accuracy)
        self.sample_count = config.getint('samples', 1, minval=1)
        self.sample_retract_dist = config.getfloat('sample_retract_dist', 2., above=0.)
        atypes = ['median', 'average']
        self.samples_result = config.getchoice('samples_result', atypes, 'average')
        self.samples_tolerance = config.getfloat('samples_tolerance', 0.100, minval=0.)
        self.samples_retries = config.getint('samples_tolerance_retries', 0, minval=0)
        # Session state
        self.multi_probe_pending = False
        self.results = []
        # Register event handlers
        self.printer.register_event_handler("gcode:command_error",
                                            self._handle_command_error)
    def _handle_command_error(self):
        if self.multi_probe_pending:
            try:
                self.end_probe_session()
            except:
                logging.exception("Multi-probe end")
    def _probe_state_error(self):
        raise self.printer.command_error(
            "Internal probe error - start/end probe session mismatch")

    def start_probe_session(self, gcmd):
        if self.multi_probe_pending:
            self._probe_state_error()
        self.multi_probe_pending = True
        self.results = []
        return self

    def end_probe_session(self):
        if not self.multi_probe_pending:
            self._probe_state_error()
        self.results = []
        self.multi_probe_pending = False

    def get_probe_params(self, gcmd=None):
        if gcmd is None:
            gcmd = self.dummy_gcode_cmd
        probe_speed = gcmd.get_float("PROBE_SPEED", self.probe_speed, above=0.)
        lift_speed = gcmd.get_float("LIFT_SPEED", self.lift_speed, above=0.)
        samples = gcmd.get_int("SAMPLES", self.sample_count, minval=1)
        sample_retract_dist = gcmd.get_float("SAMPLE_RETRACT_DIST", self.sample_retract_dist, above=0.)
        samples_tolerance = gcmd.get_float("SAMPLES_TOLERANCE", self.samples_tolerance, minval=0.)
        samples_retries = gcmd.get_int("SAMPLES_TOLERANCE_RETRIES", self.samples_retries, minval=0)
        samples_result = gcmd.get("SAMPLES_RESULT", self.samples_result)
        return {'probe_speed': probe_speed,
                'lift_speed': lift_speed,
                'samples': samples,
                'sample_retract_dist': sample_retract_dist,
                'samples_tolerance': samples_tolerance,
                'samples_tolerance_retries': samples_retries,
                'samples_result': samples_result}

    def _rocking_probe(self, probe_speed, direction='z-'):
        toolhead = self.printer.lookup_object('toolhead')
        probe_start = toolhead.get_position()
        (axis, sense) = direction_types[direction]
        rocking_count = 3
        rocks = 0
        rocking_speed = probe_speed
        rocking_lift_speed = rocking_speed * 2.0
        while rocks < rocking_count:
            pos = self._probe(rocking_speed, direction)
            rocking_speed = rocking_speed * 0.1
            rocking_retract_dist = rocking_speed * 3.0
            liftpos = probe_start
            liftpos[axis] = pos[axis] - sense * rocking_retract_dist
            self._move(liftpos, rocking_lift_speed)
            rocks += 1
        self.gcode.respond_info(f"Probe made contact on {axis} axis at {pos[0]},{pos[1]},{pos[2]}")
        return pos

    def _probe(self, probe_speed, direction='z-'):
        self.check_homed()
        (axis, sense) = direction_types[direction]
        pos = self._get_target_position(direction)
        try:
            epos = self.mcu_probes[axis].probing_move(pos, probe_speed)
        except self.printer.command_error as e:
            reason = str(e)
            if "Timeout during endstop homing" in reason:
                reason += HINT_TIMEOUT
            raise self.printer.command_error(reason)
        return epos[:3]

    def _get_target_position(self, direction):
        toolhead = self.printer.lookup_object('toolhead')
        curtime = self.printer.get_reactor().monotonic()
        (axis, sense) = direction_types[direction]
        max_distance = self.spread * 1.8
        pos = toolhead.get_position()
        kin_status = toolhead.get_kinematics().get_status(curtime)
        if 'axis_minimum' not in kin_status or 'axis_minimum' not in kin_status:
            raise self.gcode.error(
                "Tools calibrate only works with cartesian kinematics")
        if sense > 0:
            pos[axis] = min(pos[axis] + max_distance,
                            kin_status['axis_maximum'][axis])
        else:
            pos[axis] = max(pos[axis] - max_distance,
                            kin_status['axis_minimum'][axis])
        return pos

    def check_homed(self):
        toolhead = self.printer.lookup_object('toolhead')
        curtime = self.printer.get_reactor().monotonic()
        if 'x' not in toolhead.get_status(curtime)['homed_axes'] or \
                'y' not in toolhead.get_status(curtime)['homed_axes'] or \
                'z' not in toolhead.get_status(curtime)['homed_axes']:
            raise self.printer.command_error("Must home before probe")

    def _calc_mean(self, positions):
        count = float(len(positions))
        return [sum([pos[i] for pos in positions]) / count
                for i in range(3)]

    def _calc_median(self, positions, axis):
        axis_sorted = sorted(positions, key=(lambda p: p[axis]))
        middle = len(positions) // 2
        if (len(positions) & 1) == 1:
            # odd number of samples
            return axis_sorted[middle]
        # even number of samples
        return self._calc_mean(axis_sorted[middle - 1:middle + 1])

    def _calculate_results(self, positions, samples_result, axis):
        if samples_result == 'median':
            return self._calc_median(positions, axis)
        return self._calc_mean(positions)

    def run_probe(self, gcmd, direction='z-'):
        if not self.multi_probe_pending:
            self._probe_state_error()
        params = self.get_probe_params(gcmd)
        if direction not in direction_types:
            raise self.printer.command_error("Wrong value for DIRECTION.")
        logging.info("run_probe direction = " + str(direction))

        (axis, sense) = direction_types[direction]
        logging.info("run_probe axis = %d, sense = %d" % (axis, sense))

        self.gcode.respond_info(f"Probing {axis} axis with {sense} sense")

        toolhead = self.printer.lookup_object('toolhead')
        start_position = self.printer.lookup_object('toolhead').get_position()
        retries = 0
        positions = []
        probe_speed = params['probe_speed']
        lift_speed = params['lift_speed']
        sample_count = params['samples']
        sample_retract_dist = params['sample_retract_dist']
        samples_tolerance = params['samples_tolerance']
        samples_tolerance_retries = params['samples_tolerance_retries']
        samples_result = params['samples_result']

        retries = 0
        positions = []
        while len(positions) < sample_count:
            # Probe position
            pos = self._rocking_probe(probe_speed, direction)
            positions.append(pos)
            # Check samples tolerance
            axis_positions = [p[axis] for p in positions]
            if max(axis_positions)-min(axis_positions) > samples_tolerance:
                if retries >= samples_tolerance_retries:
                    raise gcmd.error("Probe samples exceed samples_tolerance")
                gcmd.respond_info("Probe samples exceed tolerance. Retrying...")
                retries += 1
                positions = []
            # Retract
            if len(positions) < sample_count:
                liftpos = start_position
                liftpos[axis] = pos[axis] - sense * sample_retract_dist
                toolhead.manual_move(liftpos, lift_speed)
        # Calculate result
        result_position = self._calculate_results(positions, samples_result, axis)
        self.results.append(result_position)


    def pull_probed_results(self):
        res = self.results
        self.results = []
        return res

class ToolProbe:
    def __init__(self, config, probe_session: ProbeSessionHelper):
        self.printer = config.get_printer()
        self.name = config.get_name()
        self.gcode_move = self.printer.load_object(config, "gcode_move")
        self.probe_session = probe_session
        self.probe_name = config.get('probe', 'probe')
        self.travel_speed = config.getfloat('travel_speed', 10.0, above=0.)
        self.spread = config.getfloat('spread', 5.0)
        self.lower_z = config.getfloat('lower_z', 0.5)
        self.lift_z = config.getfloat('lift_z', 1.0)
        self.trigger_to_bottom_z = config.getfloat('trigger_to_bottom_z',
                                                   default=0.0)
        self.lift_speed = config.getfloat('lift_speed', self.travel_speed * 0.5)
        self.final_lift_z = config.getfloat('final_lift_z', 4.0)
        self.sensor_location = None
        self.last_result = [0., 0., 0.]
        self.last_probe_offset = 0.
        self.calibration_probe_inactive = True

        # Register commands
        self.gcode = self.printer.lookup_object('gcode')
        self.gcode.register_command('TOOL_LOCATE_SENSOR',
                                    self.cmd_TOOL_LOCATE_SENSOR,
                                    desc=self.cmd_TOOL_LOCATE_SENSOR_help)
        self.gcode.register_command('TOOL_CALIBRATE_TOOL_OFFSET',
                                    self.cmd_TOOL_CALIBRATE_TOOL_OFFSET,
                                    desc=self.cmd_TOOL_CALIBRATE_TOOL_OFFSET_help)
        self.gcode.register_command('TOOL_CALIBRATE_SAVE_TOOL_OFFSET',
                                    self.cmd_TOOL_CALIBRATE_SAVE_TOOL_OFFSET,
                                    desc=self.cmd_TOOL_CALIBRATE_SAVE_TOOL_OFFSET_help)
        self.gcode.register_command('TOOL_CALIBRATE_PROBE_OFFSET',
                                    self.cmd_TOOL_CALIBRATE_PROBE_OFFSET,
                                    desc=self.cmd_TOOL_CALIBRATE_PROBE_OFFSET_help)
        self.gcode.register_command('TOOL_CALIBRATE_QUERY_PROBE',
                                    self.cmd_TOOL_CALIBRATE_QUERY_PROBE,
                                    desc=self.cmd_TOOL_CALIBRATE_QUERY_PROBE_help)

        self.printer.add_object('tool_probe', self)

    def probe_xy(self, toolhead, top_pos, direction, gcmd, samples=None):
        offset = direction_types[direction]
        start_pos = list(top_pos)
        start_pos[offset[0]] -= offset[1] * self.spread
        toolhead.manual_move([None, None, top_pos[2] + self.lift_z],
                             self.lift_speed)
        toolhead.manual_move([start_pos[0], start_pos[1], None],
                             self.travel_speed)
        toolhead.manual_move([None, None, top_pos[2] - self.lower_z],
                             self.lift_speed)
        return self.probe_session.run_probe(gcmd, direction)[offset[0]]

    def calibrate_xy(self, toolhead, top_pos, gcmd, samples=None):
        left_x = self.probe_xy(toolhead, top_pos, 'x+', gcmd, samples=samples)
        right_x = self.probe_xy(toolhead, top_pos, 'x-', gcmd, samples=samples)
        near_y = self.probe_xy(toolhead, top_pos, 'y+', gcmd, samples=samples)
        far_y = self.probe_xy(toolhead, top_pos, 'y-', gcmd, samples=samples)
        return [(left_x + right_x) / 2., (near_y + far_y) / 2.]

    def locate_sensor(self, gcmd):
        toolhead = self.printer.lookup_object('toolhead')
        position = toolhead.get_position()
        downPos = self.probe_session.run_probe(gcmd, "z-")
        center_x, center_y = self.calibrate_xy(toolhead, downPos, gcmd,
                                               samples=1)

        toolhead.manual_move([None, None, downPos[2] + self.lift_z],
                             self.lift_speed)
        toolhead.manual_move([center_x, center_y, None], self.travel_speed)
        center_z = self.probe_session.run_probe(gcmd, "z-")[2]
        # Now redo X and Y, since we have a more accurate center.
        center_x, center_y = self.calibrate_xy(toolhead,[center_x, center_y, center_z],gcmd)

        # rest above center
        position[0] = center_x
        position[1] = center_y
        position[2] = center_z + self.final_lift_z
        toolhead.manual_move([None, None, position[2]], self.lift_speed)
        toolhead.manual_move([position[0], position[1], None],
                             self.travel_speed)
        toolhead.set_position(position)
        return [center_x, center_y, center_z]

    cmd_TOOL_LOCATE_SENSOR_help = ("Locate the tool calibration sensor, "
                                   "use with tool 0.")
    def cmd_TOOL_LOCATE_SENSOR(self, gcmd):
        self.last_result = self.locate_sensor(gcmd)
        self.sensor_location = self.last_result
        self.gcode.respond_info("Sensor location at %.6f,%.6f,%.6f"
                                % (self.last_result[0], self.last_result[1],
                                   self.last_result[2]))

    cmd_TOOL_CALIBRATE_TOOL_OFFSET_help = "Calibrate current tool offset relative to tool 0"
    def cmd_TOOL_CALIBRATE_TOOL_OFFSET(self, gcmd):
        if not self.sensor_location:
            raise gcmd.error(
                "No recorded sensor location, please run TOOL_LOCATE_SENSOR first")
        location = self.locate_sensor(gcmd)
        self.last_result = [location[i] - self.sensor_location[i] for i in
                            range(3)]
        self.gcode.respond_info("Tool offset is %.6f,%.6f,%.6f"
                                % (self.last_result[0], self.last_result[1],
                                   self.last_result[2]))

    cmd_TOOL_CALIBRATE_SAVE_TOOL_OFFSET_help = "Save tool offset calibration to config"
    def cmd_TOOL_CALIBRATE_SAVE_TOOL_OFFSET(self, gcmd):
        if not self.last_result:
            gcmd.error(
                "No offset result, please run TOOL_CALIBRATE_TOOL_OFFSET first")
            return
        section_name = gcmd.get("SECTION")
        param_name = gcmd.get("ATTRIBUTE")
        template = gcmd.get("VALUE", "{x:0.6f}, {y:0.6f}, {z:0.6f}")
        value = template.format(x=self.last_result[0], y=self.last_result[1],
                                z=self.last_result[2])
        configfile = self.printer.lookup_object('configfile')
        configfile.set(section_name, param_name, value)

    cmd_TOOL_CALIBRATE_PROBE_OFFSET_help = "Calibrate the tool probe offset to nozzle tip"
    def cmd_TOOL_CALIBRATE_PROBE_OFFSET(self, gcmd):
        toolhead = self.printer.lookup_object('toolhead')
        probe = self.printer.lookup_object(self.probe_name)
        start_pos = toolhead.get_position()
        nozzle_z = self.probe_multi_axis.run_probe("z-", gcmd, speed_ratio=0.5)[
            2]
        # now move down with the tool probe
        probe_session = probe.start_probe_session(gcmd)
        probe_session.run_probe(gcmd)
        probe_z = probe_session.pull_probed_results()[0][2]
        probe_session.end_probe_session()

        z_offset = probe_z - nozzle_z + self.trigger_to_bottom_z
        self.last_probe_offset = z_offset
        self.gcode.respond_info(
            "%s: z_offset: %.3f\n"
            "The SAVE_CONFIG command will update the printer config file\n"
            "with the above and restart the printer." % (
            self.probe_name, z_offset))
        config_name = gcmd.get("PROBE", default=self.probe_name)
        if config_name:
            configfile = self.printer.lookup_object('configfile')
            configfile.set(config_name, 'z_offset', "%.6f" % (z_offset,))
        # back to start pos
        toolhead.move(start_pos, self.travel_speed)
        toolhead.set_position(start_pos)

    def get_status(self, eventtime):
        return {'last_result': self.last_result,
                'last_probe_offset': self.last_probe_offset,
                'calibration_probe_inactive': self.calibration_probe_inactive,
                'last_x_result': self.last_result[0],
                'last_y_result': self.last_result[1],
                'last_z_result': self.last_result[2]}

    cmd_TOOL_CALIBRATE_QUERY_PROBE_help = "Return the state of calibration probe"
    def cmd_TOOL_CALIBRATE_QUERY_PROBE(self, gcmd):
        toolhead = self.printer.lookup_object('toolhead')
        print_time = toolhead.get_last_move_time()
        endstop_states = [probe.query_endstop(print_time) for probe in self.probe_session.mcu_probes] # Check the state of each axis probe (x, y, z)
        self.calibration_probe_inactive = any(endstop_states)
        gcmd.respond_info("Calibration Probe: %s" % (["open", "TRIGGERED"][any(endstop_states)]))


# Main external probe interface
class PrinterProbe:
    def __init__(self, config):
        self.printer = config.get_printer()
        self.mcu_probes = [
            ProbeEndstopWrapper(config, 'x'),
            ProbeEndstopWrapper(config, 'y'),
            ProbeEndstopWrapper(config, 'z')
            ]
        self.cmd_helper = ProbeCommandHelper(config, self.mcu_probes)
        self.probe_offsets = ProbeOffsetsHelper(config)
        self.probe_session = ProbeSessionHelper(config, self.mcu_probes)
        self.tool_probe = ToolProbe(config, self.probe_session)
    def get_probe_params(self, gcmd=None):
        return self.probe_session.get_probe_params(gcmd)
    def get_offsets(self):
        return self.probe_offsets.get_offsets()
    def get_status(self, eventtime):
        return self.cmd_helper.get_status(eventtime)
    def start_probe_session(self, gcmd):
        return self.probe_session.start_probe_session(gcmd)

def load_config(config):
    return PrinterProbe(config)
