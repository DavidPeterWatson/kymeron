class Dock:
    def __init__(self, config):
        self.printer = config.get_printer()
        self.name = config.get_name().split(' ')[-1]
        self.safe_y = config.get('safe_y')
        self.move_z = config.get('safe_zd')
        self.load_y = config.get('load_yd')
        self.load_x = config.get('load_xd')
        self.loading_speed = config.get('loading_speed')


def load_config_prefix(config):
    return Dock(config)
