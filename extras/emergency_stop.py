LONG_PRESS_DURATION = 0.800
TIMER_DELAY = .200

class EmergencyStop:
    def __init__(self, config):
        self.printer = config.get_printer()
        self.name = config.get_name().split(' ')[-1]
        buttons = self.printer.load_object(config, "buttons")

        # Register kill button
        self.register_button(config, 'kill_pin', self.kill_callback)
        self.printer.add_object('emergency_stop_' + self.name, self)

    def register_button(self, config, name, callback):
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

    def kill_callback(self, eventtime):
        self.printer.invoke_shutdown("Shutdown due to emergency stop!")

def load_config_prefix(config):
    return EmergencyStop(config)
