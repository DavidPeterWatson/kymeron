class Carriage:
    def __init__(self, config):
        self.printer = config.get_printer()
        self.name = config.get_name().split(' ')[-1]
        Carriage.validate_name(self.name)
        self.berth = config.get('berth')
        self.tool_number = config.get('tool_number')
        self.offset_x = float(config.get('offset_x') or 0)
        self.offset_y = float(config.get('offset_y') or 0)
        self.offset_z = float(config.get('offset_z') or 0)
        self.loaded_button = config.get('loaded_button')
        self.calibrated = False
        self.printer.add_object('carriage ' + self.name, self)
        self.before_load_gcode = config.get('before_load_gcode', 'RESPOND MSG=Loading')
        self.before_unload_gcode = config.get('before_unload_gcode', 'RESPOND MSG=Unloading')
        self.after_load_gcode = config.get('after_load_gcode', 'RESPOND MSG=Loaded')
        self.after_unload_gcode = config.get('after_unload_gcode', 'RESPOND MSG=Unloaded')

    def validate_name(name):
        if name == 'none':
            raise Exception("Carriage name cannot be 'none'")
        if name == '':
            raise Exception("Carriage name cannot be ''")
        if not name:
            raise Exception("Carriage name cannot be '{name}'")


def load_config_prefix(config):
    return Carriage(config)
