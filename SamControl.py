import sys

import select
import serial

import datetime

from modules import StdinTools

"""

This has the main function for controlling camera, arduino, and stdin


"""



class SamControl:

    # Open ports and files
    arduino = None
    log_file = None

    # This is the dictionary that holds modules.
    # Modules need...
    local_modules = {}
    arduino_modules = {}



    def main(self):
        """

        Main method for running robot.

        """

        # Array of filenumbers for
        listening_to = []

        import serial.tools.list_ports
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            if p[1] == 'Arduino Uno':
                self.arduino = serial.Serial(p[0])

        listening_to.append(sys.stdin)
        listening_to.append(self.arduino)

        # Todo:
        # Make dictionary where if it is local, it will run the local module.
        # If it received arduino, it will get the first string and run that arduino module.

        run_mod = {}

        while True:

            responded = select.select(listening_to, [], [], .5)

            quit_program = False

            for response in responded:
                if response == sys.stdin:
                    str_rsv: str = sys.stdin.readline()
                    quit_program = self.local_modules.get(">").run(str_rsv)

                # Add here for camera --
                #elif camera:
                # quit_program = self.local_modules.get("camera_id").run(str_rsv)

                elif response == self.arduino:
                    quit_program = self.arduino_modules.get(str_rsv.strip().split(" ")).run(str_rsv)
                else:
                    print("ERROR")

                if quit_program:
                    return

    def exit(self):
        """
        And of program functions, like closing ports.
        :return: None
        """
        if self.log_file is not None:
            self.log_file.close()
        if self.arduino is not None:
            self.arduino.close()


    def init_mods(self):
        """
        Imports files in the modules folder and initiates them.
        :return: None
        """
        args_for_mods = {
            "sam": self,
            "arduino_object": self.arduino
        }

        mods = [StdinTools.StdinTools(**args_for_mods)]

        for mod in mods:
            if mod.is_local_to_pi:
                if mod.identifier in self.local_modules.keys():
                    print("Identifier " + mod.identifier +
                          " is used twice in local modules. Overwriting the first instance.")
                self.local_modules[mod.identifier] = mod
            else:
                if mod.identifier in self.arduino_modules.keys():
                    print("Identifier " + mod.identifier +
                          " is used twice in arduino modules. Overwriting the first instance.")

                self.arduino_modules[mod.identifier] = mod

    def send(self, message):
        """
        Use this function to send messages to the arduino.

        :return:
        """
        self.arduino.write(message)

    def log_to_file(self, msg, mod_name="UNK"):
        """
        Logging to a file
        :return:
        """
        while log_file is None:
            file_name_uncleansed = sys.raw_input("Enter Filename(or quit): ")
            file_name = file_name_uncleansed.strip()

            if file_name == "quit":
                return

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
    sam = SamControl()
    try:
        sam.main()
    except Exception:
        sam.exit()

