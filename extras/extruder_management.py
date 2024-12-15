class ExtruderManagement:
    def __init__(self, config):
        self.printer = config.get_printer()
        self.hot_zone_retract_length = float(config.get('hot_zone_retract_length') or 20)
        self.hot_zone_retract_speed = float(config.get('hot_zone_retract_speed') or 80)
        self.purge_length = float(config.get('purge_length') or 10)
        self.brush_movement = float(config.get('brush_movement') or 20)
        self.brush_shift = float(config.get('brush_shift') or 10)
        self.printer.add_object('extruder_management', self)


def load_config_prefix(config):
    return ExtruderManagement(config)
