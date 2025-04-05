class WiggleRetraction:
    def __init__(self, config):
        self.printer = config.get_printer()
        self.hot_zone_retract_length = float(config.get('hot_zone_retract_length') or 20)
        self.hot_zone_retract_speed = float(config.get('hot_zone_retract_speed') or 80)
        self.retract_xy_wiggle = float(config.get('retract_xy_wiggle') or 2)
        self.retract_z = float(config.get('retract_z') or 0.1)
        self.retract_length = float(config.get('retract_length') or 3)
        self.unretract_extra_length = float(config.get('unretract_extra_length') or 0.0)
        self.retract_speed = float(config.get('retract_speed') or 100)
        self.unretract_dwell = float(config.get('unretract_dwell') or 0.1)
        self.unretract_speed = float(config.get('unretract_speed') or 100)
        self.printer.add_object('retraction', self)


def load_config(config):
    return WiggleRetraction(config)
