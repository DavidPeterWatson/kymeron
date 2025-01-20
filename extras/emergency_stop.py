import logging

class EmergencyStop:
    def __init__(self, config):
        self.printer = config.get_printer()
        self.name = config.get_name().split(' ')[-1]
        self.pin = config.get('pin')
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
        self.gcode.register_mux_command("QUERY_EMERGENCY", "BUTTON", self.name,
                                        self.cmd_QUERY_BUTTON,
                                        desc=self.cmd_QUERY_BUTTON_help)

    cmd_QUERY_BUTTON_help = "Report on the state of a button"
    def cmd_QUERY_BUTTON(self, gcmd):
        gcmd.respond_info(self.name + ": " + self.get_status()['state'])

    def button_callback(self, eventtime, state):
        self.last_state = state
        try:
            gcode = self.printer.lookup_object('gcode')
            if state:
                gcode.respond_info("emergency stop activated!")
            else:
                gcode.respond_info("emergency stop deactivated!")
        except:
            logging.exception("Script running error")

    def get_status(self, eventtime=None):
        if self.last_state:
            return {'state': "PRESSED"}
        return {'state': "RELEASED"}

def load_config_prefix(config):
    return EmergencyStop(config)
