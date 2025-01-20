import logging


class EmergencyStop:
    def __init__(self, config):
        gcode = self.printer.lookup_object('gcode')
        try:
            self.printer = config.get_printer()
            self.name = config.get_name().split(' ')[-1]

            # Register kill button
            self.register_button(config, 'kill_pin', self.kill_callback)
            self.printer.add_object('emergency_stop_' + self.name, self)
        except Exception as e:
            reason = str(e)
            gcode.respond_info(f"Error initialising emergency button. {reason}")
            raise e


    def register_button(self, config, name, callback):
        gcode = self.printer.lookup_object('gcode')
        try:
            pin = config.get(name, None)
            if pin is None:
                return
            buttons = self.printer.lookup_object("buttons")
            if config.get('analog_range', None) is None:
                buttons.register_buttons([pin], callback)
                return
            amin, amax = config.getfloatlist('analog_range', count=2)
            pullup = config.getfloat('analog_pullup_resistor', 4700., above=0.)
            buttons.register_adc_button(pin, amin, amax, pullup, callback)
        except Exception as e:
            reason = str(e)
            gcode.respond_info(f"Error registering emergency button. {reason}")
            raise e

    def kill_callback(self, eventtime):
        gcode = self.printer.lookup_object('gcode')
        gcode.respond_info("emergency stop activated!")
        # self.printer.invoke_shutdown("Shutdown due to emergency stop!")
        

def load_config_prefix(config):
    return EmergencyStop(config)
