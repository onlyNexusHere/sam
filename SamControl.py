import sys

import select
import serial.tools.list_ports
from modules import StdinTools, CameraProcessing, ArduinoDebug, Ping, Motors

# import os.path
# if os.path.isfile("/proc/cpuinfo"):
#     from picamera import PiCamera
# else:
#     PiCamera = None

"""

This has the main function for controlling camera, arduino, and stdin


"""


class SamControl:

    # Open ports and files
    arduino = None
    log_file = None
    camera = None
    debug = False

    # This is the dictionary that holds modules.
    # Modules need...
    local_modules = {}
    arduino_modules = {}

    quit_program = False

    # Array of file numbers for
    listening_to = []

    def main(self):
        """

        Main method for running robot.

        """
        self.find_arduino()
        self.init_mods()

        if self.debug: print("Everything has been initialized")

        while self.quit_program is False:

            if self.debug: print("Starting to listen")

            responded = select.select(self.listening_to, [], [], .5)[0]

            if self.debug: print("Select started")

            for response in responded:
                if response == sys.stdin:
                    str_rsv = sys.stdin.readline()
                    if self.debug: print("got message: " + str_rsv)
                    self.local_modules.get(">").message_received(str_rsv)

                elif response == self.arduino:
                    if self.debug: print("Arduino sent a message.")
                    arduino_says = response.readline()
                    if self.debug: print("Messsage:" + arduino_says.decode("utf-8").strip())
                    module_to_use = self.arduino_modules.get(arduino_says.decode("utf-8").strip().split(" ")[0].lower(), None)
                    if module_to_use is not None:
                        module_to_use.message_received(arduino_says.decode("utf-8").strip())
                    else:
                        if self.debug: print("Received incorrect module " + arduino_says.decode("utf-8").strip().split(" ")[0])
                else:
                    print("ERROR")

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
        if self.debug: print("Debug getting modules")

        args_for_mods = {
            "sam": self,
            "arduino_object": self.arduino,
            "log_file": self.log_file
        }

        if self.debug: print("About to initialize mods")

        mods = [StdinTools.StdinTools(args_for_mods),
                CameraProcessing.CameraProcessing(args_for_mods),
                ArduinoDebug.ArduinoDebug(args_for_mods),
                Ping.Ping(args_for_mods),
                Motors.Motors(args_for_mods)]

        if self.debug: print("mods initialized")

        for mod in mods:
            if self.debug: print("initializing " + mod.identifier)

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

        if self.debug: print("Debug imported modules")

    def find_arduino(self):
        print("Finding Arduino USB")

        if self.debug: print("Debug 1")

        ports = list(serial.tools.list_ports.comports())
        print("Looking at all ports")
        for p in ports:
            if self.debug: print("Going to next port")
            if "Arduino" in p[1]:
                try:
                    self.arduino = serial.Serial(p[0])
                except serial.serialutil.SerialException:
                    print("Could not connect to Arduino, either permissions or its busy")
                if self.debug: print("Arduino USB was found at " + p[0])

                # Adding listeners to the list
        if self.debug: print("Done looking through ports")
        if self.arduino is not None:
            self.listening_to.append(self.arduino)
        else:
            print("Arduino USB was not found.")
        self.listening_to.append(sys.stdin)


    def send(self, message):
        """
        Use this function to send messages to the arduino.

        :return:
        """
        if self.arduino is not None:
            self.arduino.write(message)
        else:
            print("Arduino is not connected!")

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

