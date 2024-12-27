# Nozzle alignment module for 3d kinematic probes.
#
# This module has been adapted from code written by Kevin O'Connor <kevin@koconnor.net> and Martin Hierholzer <martin@hierholzer.info>
# Sourced from https://github.com/ben5459/Klipper_ToolChanger/blob/master/probe_multi_axis.py

import logging
import time

direction_types = {'x+': [0, +1], 'x-': [0, -1], 'y+': [1, +1], 'y-': [1, -1],
                   'z+': [2, +1], 'z-': [2, -1]}

HINT_TIMEOUT = """
If the probe did not move far enough to trigger, then
consider reducing/increasing the axis minimum/maximum
position so the probe can travel further (the minimum
position can be negative).
"""


class ToolProbe:
    def __init__(self, config):
        self.printer = config.get_printer()
        self.name = config.get_name()
        self.gcode_move = self.printer.load_object(config, "gcode_move")
        self.probe_name = config.get('probe', 'probe')
        self.probe = self.printer.load_object(config, self.probe_name)

        self.travel_speed = config.getfloat('travel_speed', 10.0, above=0.)
        self.spread = config.getfloat('spread', 5.0)
        self.lower_z = config.getfloat('lower_z', 0.5)
        self.lift_z = config.getfloat('lift_z', 1.0)
        self.trigger_to_bottom_z = config.getfloat('trigger_to_bottom_z', default=0.0)
        self.final_lift_z = config.getfloat('final_lift_z', 4.0)
        self.sensor_location = None
        self.last_result = [0., 0., 0.]
        self.last_probe_offset = 0.
        self.calibration_probe_inactive = True

        # Register commands
        self.gcode = self.printer.lookup_object('gcode')
        self.gcode.register_command('LOCATE_TOOL_PROBE',
                                    self.cmd_LOCATE_TOOL_PROBE,
                                    desc=self.cmd_LOCATE_TOOL_PROBE_help)
        self.gcode.register_command('CALIBRATE_TOOL_OFFSET',
                                    self.cmd_CALIBRATE_TOOL_OFFSET,
                                    desc=self.cmd_CALIBRATE_TOOL_OFFSET_help)
        self.gcode.register_command('QUERY_TOOL_PROBE',
                                    self.cmd_QUERY_TOOL_PROBE,
                                    desc=self.cmd_QUERY_TOOL_PROBE_help)

    cmd_LOCATE_TOOL_PROBE_help = ("Locate the tool probe with bed probe")
    def cmd_LOCATE_TOOL_PROBE(self, gcmd):
        self.last_result = self.locate_sensor(gcmd)
        self.sensor_location = self.last_result
        self.gcode.respond_info("Sensor location at %.6f,%.6f,%.6f"
                                % (self.last_result[0], self.last_result[1],
                                   self.last_result[2]))

    cmd_CALIBRATE_TOOL_OFFSET_help = "Calibrate current tool offset relative to tool probe"
    def cmd_CALIBRATE_TOOL_OFFSET(self, gcmd):
        if not self.sensor_location:
            raise gcmd.error(
                "No recorded sensor location, please run TOOL_LOCATE_SENSOR first")
        location = self.locate_sensor(gcmd)
        self.last_result = [location[i] - self.sensor_location[i] for i in
                            range(3)]
        self.gcode.respond_info("Tool offset is %.6f,%.6f,%.6f"
                                % (self.last_result[0], self.last_result[1],
                                   self.last_result[2]))

    def locate_sensor(self, gcmd):
        toolhead = self.printer.lookup_object('toolhead')
        position = toolhead.get_position()
        downPos = self.probe.probe_session.run_probe(gcmd, "z-") # samples = 1
        center_x, center_y = self.calibrate_xy(toolhead, downPos, gcmd, samples=1)

        toolhead.manual_move([None, None, downPos[2] + self.lift_z],
                             self.travel_speed)
        toolhead.manual_move([center_x, center_y, None], self.travel_speed)
        center_z = self.probe.probe_session.run_probe("z-", gcmd, speed_ratio=0.5)[
            2]
        # Now redo X and Y, since we have a more accurate center.
        center_x, center_y = self.calibrate_xy(toolhead,
                                               [center_x, center_y, center_z],
                                               gcmd)

        # rest above center
        position[0] = center_x
        position[1] = center_y
        position[2] = center_z + self.final_lift_z
        toolhead.manual_move([None, None, position[2]], self.travel_speed)
        toolhead.manual_move([position[0], position[1], None], self.travel_speed)
        toolhead.set_position(position)
        return [center_x, center_y, center_z]

    def calibrate_xy(self, toolhead, top_pos, gcmd):
        left_x = self.probe_xy(toolhead, top_pos, 'x+', gcmd)
        right_x = self.probe_xy(toolhead, top_pos, 'x-', gcmd)
        near_y = self.probe_xy(toolhead, top_pos, 'y+', gcmd)
        far_y = self.probe_xy(toolhead, top_pos, 'y-', gcmd)
        return [(left_x + right_x) / 2., (near_y + far_y) / 2.]

    def probe_xy(self, toolhead, top_pos, direction, gcmd):
        offset = direction_types[direction]
        start_pos = list(top_pos)
        start_pos[offset[0]] -= offset[1] * self.spread
        toolhead.manual_move([None, None, top_pos[2] + self.lift_z], self.travel_speed)
        toolhead.manual_move([start_pos[0], start_pos[1], None], self.travel_speed)
        toolhead.manual_move([None, None, top_pos[2] - self.lower_z], self.travel_speed)
        return self.probe.probe_session.run_probe(gcmd, direction)[offset[0]]

    def get_status(self):
        return {'last_result': self.last_result,
                'last_probe_offset': self.last_probe_offset,
                'calibration_probe_inactive': self.calibration_probe_inactive,
                'last_x_result': self.last_result[0],
                'last_y_result': self.last_result[1],
                'last_z_result': self.last_result[2]}

    cmd_QUERY_TOOL_PROBE_help = "Return the state of calibration probe"
    def cmd_QUERY_TOOL_PROBE(self, gcmd):
        toolhead = self.printer.lookup_object('toolhead')
        print_time = toolhead.get_last_move_time()
        endstop_states = [probe.query_endstop(print_time) for probe in self.probe.mcu_probes] # Check the state of each axis probe (x, y, z)
        self.calibration_probe_inactive = any(endstop_states)
        gcmd.respond_info("Calibration Probe: %s" % (["open", "TRIGGERED"][any(endstop_states)]))

def load_config(config):
    return ToolProbe(config)
