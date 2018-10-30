import sys

import select
import serial.tools.list_ports
import datetime
from modules import StdinTools

import os.path
if os.path.isfile("/proc/cpuinfo"):
    from picamera import PiCamera
else:
    PiCamera = None

"""

This has the main function for controlling camera, arduino, and stdin


"""


class SamControl:

    # Open ports and files
    arduino = None
    log_file = None
    camera = None

    # This is the dictionary that holds modules.
    # Modules need...
    local_modules = {}
    arduino_modules = {}

    quit_program = False

    def main(self):
        """

        Main method for running robot.

        """

        # Array of file numbers for
        listening_to = []

        self.init_mods()

        print("Finding Arduino USB")

        print("1")
        ports = list(serial.tools.list_ports.comports())
        print("2")
        for p in ports:
            print("3")
            if "Arduino" in p[1]:
                print("4")
                self.arduino = serial.Serial(p[0])
                print("Arduino USB was found at " + p[0])

                # Adding listeners to the list
            print("7")
        print("6")
        if self.arduino is not None:
            listening_to.append(self.arduino)
        else:
            print("Arduino USB was not found.")
        print("7")
        listening_to.append(sys.stdin)

        # CAMERA MODULE PART 1 - add the camera interface object
        #self.camera = ...

        if self.camera is not None:
            listening_to.append(self.camera)
        else:
            print("Camera was not found.")

                # This is the heart of the program. Select is non-blocking.
        print("8")
        while self.quit_program is False:
            print("9")
            responded = select.select(listening_to, [], [], .5)[0]
            print("10")
            for response in responded:
                print("11")
                if response == sys.stdin:
                    print("12")
                    str_rsv: str = sys.stdin.readline()
                    # print("got message: " + str_rsv)
                    self.local_modules.get(">").message_received(str_rsv)
                    print("13")
                # CAMERA MODULE PART 2 - code commented out below is not correct, but has the general idea.
                # Please add code like the stuff below.
                elif response == self.camera:
                    # str_rsv = camera.read
                    # self.local_modules.get("camera_id").message_received(str_rsv)
                    pass

                elif response == self.arduino:
                    print("15")
                    str_rsv = self.arduino.readline() # This will read one byte. We can change it as needed.
                    print("16")
                    self.arduino_modules.get(str_rsv.strip().split(" "), None).message_received(str_rsv)
                    print("17")
                else:
                    print("ERROR")
                print("14")
                if self.quit_program:
                    print("Goodbye!")
                    return
            [mod.on_wait() for _, mod in {**self.local_modules, **self.arduino_modules}.items()]

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

        # This is where we add the new mods for proper initialization.
        # Remember to use **args for mods as the parameter to initialize the mod.
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
        if self.arduino is not None:
            self.arduino.write(message)
        else:
            print("Arduino is not connected!")

    def log_to_file(self, msg, mod_name="UNK"):
        """
        Logging to a file
        :return:
        """
        while self.log_file is None:
            file_name_uncleansed = sys.raw_input("Enter Filename(or quit): ")
            file_name = file_name_uncleansed.strip()

            if file_name == "quit":
                return

            self.log_file = open(file_name, 'a')

        log_message = "\n" + str(datetime.datetime.now()) + " " + mod_name + ": " + msg

        self.log_file.write(log_message)


    def write_to_stdout(self, mod_name="Default", msg=""):
        """

        :param mod_name: Name of module needed.
        :param msg:
        :return:
        """
        print(mod_name + " " + msg)

    def request_quit(self):
        """Use this function to kill the robot's program. Any mod can do this if needed."""
        self.quit_program = True

    class Sam_Control_Error(Exception):
        """Base error class"""
        pass

    class Arduino_Error(Sam_Control_Error):
        pass


if __name__ == "__main__":
    sam = SamControl()
    try:
        print("Running main")
        sam.main()
    except Exception:
        sam.exit()

