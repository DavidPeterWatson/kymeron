import logging

class EmergencyStop:
    def __init__(self, config):
        self.printer = config.get_printer()
        self.name = config.get_name().split(' ')[-1]
        self.pin = config.get('pin')
        self.enabled = config.get('enabled', True)
        self.last_state = 0
        buttons = self.printer.load_object(config, "buttons")
        if config.get('analog_range', None) is None:
            buttons.register_buttons([self.pin], self.button_callback)
        else:
            amin, amax = config.getfloatlist('analog_range', count=2)
            pullup = config.getfloat('analog_pullup_resistor', 4700., above=0.)
            buttons.register_adc_button(self.pin, amin, amax, pullup,
                                        self.button_callback)

        self.gcode = self.printer.lookup_object('gcode')
        self.gcode.register_mux_command("QUERY_EMERGENCY", "EMERGENCY_STOP", self.name,
            self.cmd_QUERY_EMERGENCY,
            desc=self.cmd_QUERY_EMERGENCY_help)
        self.gcode.register_mux_command("ENABLE_EMERGENCY", "EMERGENCY_STOP", self.name,
            self.cmd_ENABLE_EMERGENCY_STOP,
            desc=self.cmd_ENABLE_EMERGENCY_STOP_help)
        self.gcode.register_mux_command("DISABLE_EMERGENCY_STOP", "EMERGENCY_STOP", self.name,
            self.cmd_DISABLE_EMERGENCY_STOP,
            desc=self.cmd_DISABLE_EMERGENCY_STOP_help)

    cmd_QUERY_EMERGENCY_help = "Report on the state of an emergency stop"
    def cmd_QUERY_EMERGENCY(self, gcmd):
        gcmd.respond_info(self.name + ": " + self.get_status()['state'])

    cmd_ENABLE_EMERGENCY_STOP_help = "Enable the emergency stop"
    def cmd_ENABLE_EMERGENCY_STOP(self, gcmd):
        self.enabled = True
        gcmd.respond_info("emergency stop enabled!")

    cmd_DISABLE_EMERGENCY_STOP_help = "Disable the emergency stop"
    def cmd_DISABLE_EMERGENCY_STOP(self, gcmd):
        self.enabled = False
        gcmd.respond_info("emergency stop disabled!")

    def button_callback(self, eventtime, state):
        self.last_state = state
        gcode = self.printer.lookup_object('gcode')
        if state:
            gcode.respond_info("emergency stop activated!")
            if self.enabled:
                self.printer.invoke_shutdown("Shutdown due to emergency stop!")
        else:
            gcode.respond_info("emergency stop deactivated!")


    def get_status(self, eventtime=None):
        if self.last_state:
            return {'state': "PRESSED"}
        return {'state': "RELEASED"}

def load_config_prefix(config):
    return EmergencyStop(config)
