import sys
import argparse
import select
import serial.tools.list_ports
from modules import StdinTools, CameraProcessing, ArduinoDebug, Ping, Motors
from datetime import datetime


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

    def __init__(self, log_file=None, arduino_location=None):
        if log_file is not None:
            try:
                self.log_file = open(log_file[0], "a")
            except:
                print("Cannot open log_file" + log_file)
        if arduino_location is not None:
            try:
                self.arduino = serial.Serial(arduino_location[0])

            except serial.serialutil.SerialException:
                print("Could not connect to Arduino, either permissions or its busy")

    def main(self):
        """

        Main method for running robot.

        """
        if self.arduino is None:
            self.find_arduino()

        self.init_mods()

        if self.debug:
            print("Everything has been initialized")

        while self.quit_program is False:

            if self.debug:
                print("Starting to listen")

            responded = select.select(self.listening_to, [], [], .5)[0]

            if self.debug:
                print("Select started")

            for response in responded:

                if response == sys.stdin:
                    self._process_stdin()

                elif response == self.arduino:
                    if self.debug:
                        print("Arduino sent a message.")
                    self._process_arduino_message(response)

                else:
                    print("ERROR")

                if self.quit_program:
                    print("Goodbye!")
                    return

            if self.debug: print("Running on wait commands.")
            for _, mod in {**self.local_modules, **self.arduino_modules}.items():
                try:
                    mod.on_wait()
                except Exception as e:
                    print("Exception found in module " + mod.name + " for on wait\n" + str(e))

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
        self.debug_run(print, "Debug getting modules")

        args_for_mods = {
            "sam": self,
            "arduino_object": self.arduino,
            "log_file": self.log_file
        }

        self.debug_run(print, "About to initialize mods")

        mods = [StdinTools.StdinTools(args_for_mods),
                CameraProcessing.CameraProcessing(args_for_mods),
                ArduinoDebug.ArduinoDebug(args_for_mods),
                Ping.Ping(args_for_mods),
                Motors.Motors(args_for_mods)]

        self.debug_run(print, "mods initialized")

        for mod in mods:
            self.debug_run(print, "initializing " + mod.identifier)

            if mod.identifier is "":
                print("Cannot initialize a module. Module " + mod.name + " is missing an identifier.")
                break

            if mod.name is "":
                print("Cannot initialize a module. Module is missing a name. Id: " + mod.identifier)
                break

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

        self.debug_run(print, "Debug imported modules")

    def find_arduino(self):
        self.debug_run(print, "Finding Arduino USB")

        self.debug_run(print, "Debug 1")

        ports = list(serial.tools.list_ports.comports())
        self.debug_run(print, "Looking at all ports")
        for p in ports:
            self.debug_run(print, "Going to next port")
            if "Arduino" in p[1]:
                try:
                    self.arduino = serial.Serial(p[0])
                except serial.serialutil.SerialException:
                    print("Could not connect to Arduino, either permissions or its busy")
                print("Arduino USB was found at " + p[0])

                # Adding listeners to the list
        self.debug_run(print, "Done looking through ports")
        if self.arduino is not None:
            self.listening_to.append(self.arduino)
        else:
            print("Arduino USB was not found.")
        self.listening_to.append(sys.stdin)

    def _process_stdin(self):

        str_rsv = sys.stdin.readline()

        self.debug_run(print, "got message: " + str_rsv)

        try:
            self.local_modules.get(">").message_received(str_rsv)
        except Exception as e:
            print("Exception found in stdin module for message received\n" + str(e))

    def _process_arduino_message(self, response):

        try:
            arduino_says = response.readline()
        except Exception as e:
            print(str(e))
            return

        self.debug_run(print, "Messsage:" + arduino_says.decode("utf-8", 'ignore').strip())

        module_to_use = self.arduino_modules.get(arduino_says.decode("utf-8", 'ignore').strip().split(" ")[0].lower(), None)

        if module_to_use is not None:
            try:
                module_to_use.message_received(" ".join(arduino_says.decode("utf-8", 'ignore').strip().split(" ")[1:]))
            except Exception as e:
                print("Exception found in module " + module_to_use.name + " for message received\n" + str(e))
        else:
            self.debug_run(print, "Received incorrect module " + arduino_says.decode("utf-8").strip().split(" ")[0])

    def send(self, message):
        """
        Use this function to send messages to the arduino.

        :return:
        """
        if self.arduino is not None:
            self.debug_run(print, "Sending arduino message: " + message)

            self.arduino.write(message.encode("utf-8"))
            self.log_to_file("Sending to arduino: " + message)

            self.debug_run(print, "sent arduino message")
        else:
            print("Arduino is not connected!")

    def log_to_file(self, string_to_write):

        if self.log_file is not None:
            self.log_file.write(str(datetime.now()) + " " + string_to_write + "\n")

    def write_to_stdout(self, mod_name="Default", msg=""):
        """

        :param mod_name: Name of module needed.
        :param msg:
        :return:
        """
        print(mod_name + " " + msg)
        self.log_to_file(mod_name + " " + msg)

    def debug_run(self, func, func_args):
        """
        Function for running a command only in debugging mode.
        It takes a first order function and some type of argument,
        so either list of argument, dictionary of names arguments, or a string/int.
        :param func:
        :param func_args:
        :return:
        """
        if self.debug:
            if type(func_args) is list:
                func(*func_args)
            elif type(func_args) is dict:
                func(**func_args)
            else:
                func(func_args)


    def request_quit(self):
        """Use this function to kill the robot's program. Any mod can do this if needed."""
        self.quit_program = True

    class Sam_Control_Error(Exception):
        """Base error class"""
        pass

    class Arduino_Error(Sam_Control_Error):
        pass


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Run the SAM robot.")
    parser.add_argument("--log-file", nargs=1, type=str,
                        help="Use this variable to set a log file and start logging.")
    parser.add_argument("--arduino", nargs=1, type=str,
                        help="Set the location of the arduino. Useful if there are multiple arduinos connected.")

    args = parser.parse_args()

    sam = SamControl(args.log_file, args.arduino)

    try:
        sam.main()
    except Exception as e:
        print("Sam has failed --> " + e.__doc__)
        print(str(e))
        sam.exit()

