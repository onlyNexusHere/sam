import sys

import select
import serial

import datetime

"""

This has the main function for controlling camera, arduino, and stdin


"""
# Open ports and files
arduino = None
log_file = None


class SamControl:

    # This is the dictionary that holds modules.
    # Modules need...
    modules = {}


    def main(self):
        """

        Main method for running robot.

        """

        # Array of filenumbers for
        listening_to = []

        arduino = serial.Serial('/dev/ttyUSB0')

        listening_to.append(sys.stdin)
        listening_to.append(arduino)

        while True:

            responded = select.select(listening_to, [], [], .5)

            # for n in responded:

    def init_mods(self):
        """
        Imports files in the modules folder and initiates them.
        :return: None
        """

    def send(self):
        """
        Use this function to send messages to the arduino.

        :return:
        """

    def log_to_file(self, msg, mod_name="UNK"):
        """
        Logging to a file
        :return:
        """
        while log_file is None:
            file_name_uncleansed = sys.raw_input("Enter Filename: ")
            file_name = file_name_uncleansed.strip()

            log_file = open(file_name, 'a')

        log_message = "\n" + str(datetime.datetime.now()) + " " + mod_name + ": " + msg

        log_file.write(log_message)


    def write_to_stdout(self, mod_name="Default", msg=""):
        """

        :param mod_name: Name of module needed.
        :param msg:
        :return:
        """
        print(mod_name + " " + msg)

    class Sam_Control_Error(Exception):
        """Base error class"""
        pass

    class Arduino_Error(Sam_Control_Error):
        pass


if __name__ == "__main__":
    try:
        SamControl.main()

    except Exception:
        log_file.close()
        arduino.close()

