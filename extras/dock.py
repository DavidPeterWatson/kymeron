class Dock:
    def __init__(self, config):
        self.printer = config.get_printer()
        self.name = config.get_name().split(' ')[-1]
        self.location = config.get('location')
        self.safe_y = float(config.get('safe_y') or 0)
        self.load_yd = float(config.get('load_yd') or 0)
        self.engage_xd = float(config.get('engage_xd') or 0)
        self.safe_zone_button = config.get('safe_zone_button')
        self.printer.add_object('dock ' + self.name, self)


def load_config_prefix(config):
    return Dock(config)
