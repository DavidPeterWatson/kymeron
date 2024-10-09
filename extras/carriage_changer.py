import os

class CarriageChanger:
    def __init__(self, config):
        self.printer = config.get_printer()
        self.name = 'carriage_changer'
        self.safe_z = float(config.get('safe_z') or 20)
        self.align_speed = float(config.get('align_speed')) * 60
        self.load_speed = float(config.get('load_speed')) * 60
        self.engage_speed = float(config.get('engage_speed')) * 60
        self.acceleration = float(config.get('acceleration') or 500)
        self.loading_pause = config.get('loading_pause') or 1
        self.printer.add_object('carriage_changer', self)
        # Load carriage movement
        # pconfig = self.printer.lookup_object('configfile')
        # dirname = os.path.dirname(os.path.realpath(__file__))
        # filename = os.path.join(dirname, 'carriage_movement.cfg')
        # try:
        #     carriage_movement = pconfig.read_config(filename)
        # except Exception:
        #     raise config.error("Cannot load config '%s'" % (filename,))
        # for section in carriage_movement.get_prefix_sections(''):
        #     self.printer.load_object(carriage_movement, section.get_name())

def load_config_prefix(config):
    return CarriageChanger(config)
