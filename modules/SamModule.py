

class SamModule:

    """
    Modules will inherit from this class.
    """
    arduino = None
    sam = None
    name = None

    def __init__(self, module_name="", SamControl=None, arduino_object=None):

        self.arduino = arduino_object
        self.sam = SamControl
        self.name = module_name

    def run(self):
        pass

    def write_to_stdout(self, string_to_write):
        self.sam.write_to_stdout(mod_name=self.name, msg=string_to_write)

    def log_to_file(self, string_to_log):
        self.sam.log_to_file(string_to_log, module_name=self.name)

    def send(self, msg):
        self.sam.send(msg)
