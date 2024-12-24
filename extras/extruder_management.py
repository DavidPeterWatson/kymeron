class ExtruderManagement:
    def __init__(self, config):
        self.printer = config.get_printer()
        self.purge_length = float(config.get('purge_length') or 10)
        self.printer.add_object('extruder_management', self)


def load_config(config):
    return ExtruderManagement(config)
