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
    send_id = None
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
        self.identifier = identi.lower()
        self.is_local_to_pi = is_local
        self.log_file = log_file
        self.send_id = self.identifier

    def message_received(self, message):
        """
        This function is message_received when the arduino sends a message from the module to the pi.
        Message does not include the identifier sent by the arduino
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
        self.sam.log_to_file(self.identifier + " " + string_to_log)

    def send(self, msg):
        """
        Use this function to send a message to the arduino.

        Adds the identifier
        """
        if type(msg) is bytes:
            self.write_to_stdout(self.name + " module is sending bytes, please send a string.")
            return

        # self.debug_run(self.write_to_stdout, "Sending \" " + msg + " \" to arduino")
        self.sam.send(self.send_id + " " + msg)

    def debug_run(self, func, func_args):
        """
        Use this command to run something only in debugging mode.

        :param func:
        :param func_args:
        :return:
        """
        self.sam.debug_run(func, func_args)

    def exit(self):
        """
        Use this command to close anything you may have intitialized.
        :return:
        """
        pass

