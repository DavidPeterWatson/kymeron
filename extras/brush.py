class Brush:
    def __init__(self, config):
        self.printer = config.get_printer()
        self.brush_movement = float(config.get('brush_movement') or 20)
        self.brush_shift = float(config.get('brush_shift') or 10)
        self.brush_length = float(config.get('brush_length') or 50)
        self.brush_offset = float(config.get('brush_offset') or 110)
        self.brush_x_pos = float(config.get('brush_x_pos') or 0)
        self.brush_speed = float(config.get('brush_speed') or 100)
        self.safe_z_pos_for_brush = float(config.get('safe_z_pos_for_brush') or 30)
        self.purge_length = float(config.get('purge_length') or 10)
        self.purge_speed = float(config.get('purge_speed') or 40)
        self.printer.add_object('brush', self)


def load_config(config):
    return Brush(config)
