# import SamControl
import serial
import sys
import datetime

class SamModule:

    """
    Modules will inherit from this class.
    """
    arduino = None
    sam = None
    name = None
    identifier = None
    is_local_to_pi = False
    log_file = None

    def __init__(self,
                 module_name="",
                 sam=None,
                 arduino_object=None,
                 identi="",
                 is_local=False,
                 log_file=None):

        print("Setting up " + module_name)

        self.arduino = arduino_object
        self.sam = sam
        self.name = module_name
        self.identifier = identi
        self.is_local_to_pi = is_local
        self.log_file = log_file

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
        while self.log_file is None:
            file_name_uncleansed = sys.raw_input("Enter Filename(or quit): ")
            file_name = file_name_uncleansed.strip()
            if file_name == "quit":
                return
            self.log_file = open(file_name, 'a')
        log_message = "\n" + str(datetime.datetime.now()) + " " + self.name + ": " + string_to_log
        self.log_file.write(log_message)

    def send(self, msg):
        """
        Use this function to send a message to the arduino.
        """
        self.sam.send(msg)

