# import SamControl
import serial

class SamModule:

    """
    Modules will inherit from this class.
    """
    arduino = None
    sam = None
    name = None
    identifier = None
    is_local_to_pi = False

    def __init__(self,
                 module_name="",
                 sam=None,
                 arduino_object=None,
                 identi="",
                 is_local=False):

        print("Setting up " + module_name)

        self.arduino = arduino_object
        self.sam = sam
        self.name = module_name
        self.identifier = identi
        self.is_local_to_pi = is_local

    def message_received(self, message):
        """
        This function is message_received when the arduino sends a message from the module to the pi.
        Message should include the identifier in the front.
        """
        pass

    def stdin_request(self, message):
        """
        This function is message_received when the terminal is used to request a specific module to do something.
        This string removes the 'request mod_name' from the front.
        """
        pass

    def on_wait(self):
        """
        This runs at least every .5 seconds at least.
        This method can be used to request an update regularily.
        """
        pass

    def write_to_stdout(self, string_to_write):
        """
        Use this method to print to the terminal running the program on the pi.
        """
        self.sam.write_to_stdout(mod_name=self.name, msg=string_to_write)

    def log_to_file(self, string_to_log):
        """
        Use this to write to the logging file.
        """
        self.sam.log_to_file(string_to_log, module_name=self.name)

    def send(self, msg):
        """
        Use this function to send a message to the arduino.
        """
        self.sam.send(msg)

