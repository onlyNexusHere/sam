import sys
import argparse
import select
import traceback
import serial.tools.list_ports
from modules import StdinTools, CameraProcessing, ArduinoDebug, Ping, Motors, Quadrature, SamModule
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
    debug = None

    # This is the dictionary that holds modules.
    # Modules need...
    local_modules = {}
    arduino_modules = {}

    # list of module names that are filtered out of on_wait
    broken_module_on_wait = list()

    quit_program = False

    # Array of file numbers for
    listening_to = []

    def __init__(self, log_file=None, arduino_location=None, debug=False):
        if log_file is not None:
            try:
                self.log_file = open(log_file[0], "a")
            except:
                print("Cannot open log_file" + log_file)
        if arduino_location is not None:
            try:
                self.arduino = serial.Serial(arduino_location[0], timeout=1, baudrate=115200)

            except serial.serialutil.SerialException:
                print("Could not connect to Arduino, either permissions or its busy")

        self.debug = debug

    def main(self, program=None):
        """

        Main method for running robot.

        """
        if self.arduino is None:
            self.find_arduino()

        if self.arduino is not None:
            self.listening_to.append(self.arduino)
        else:
            print("Arduino USB was not found.")

        self.listening_to.append(sys.stdin)

        self.init_mods()

        self.debug_run(print, "Everything has been initialized")

        if program is not None and len(program) > 0:
            self.debug_run(print, "Running startup file")
            self.local_modules.get(">").message_received("run " + program[0])

        self.debug_run(print, "Start non-blocking loop")
        while self.quit_program is False:
            self.process_sockets()

    def exit(self):
        """
        And of program functions, like closing ports.
        :return: None
        """
        if self.log_file is not None:
            self.log_file.close()

        if self.arduino is not None:
            self.arduino.close()

        #TODO run module exit functions. With try/catch

    def init_mods(self):
        """
        Imports files in the modules folder and initializes them.
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
                Motors.Motors(args_for_mods),
                Quadrature.Quadrature(args_for_mods)]

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
            self.debug_run(print, "Going to next port: " + str(p[0]) + " :" + str(p[1]))
            if "Arduino" in p[1]:
                try:
                    self.arduino = serial.Serial(p[0], timeout=1, baudrate=115200)
                except serial.serialutil.SerialException:
                    print("Could not connect to Arduino, either permissions or its busy")
                print("Arduino USB was found at " + p[0])

                # Adding listeners to the list
        self.debug_run(print, "Done looking through ports")


    def _send_code_to_arduino(self, location_of_file):
        pass

    def process_sockets(self):
        # self.debug_run(print, "Starting to listen")

        responded = select.select(self.listening_to, [], [], .02)[0]

        # self.debug_run(print, "Select started")

        for response in responded:

            if response == sys.stdin:
                self.debug_run(print, "Stdin sent a message.")
                self._process_stdin()

            elif response == self.arduino:
                self.debug_run(print, "Arduino sent a message.")
                self._process_arduino_message(response)

            else:
                print("ERROR")

            if self.quit_program:
                print("Goodbye!")
                return

        # self.debug_run(print, "Running on_wait commands.")
        for _, mod in {**self.local_modules, **self.arduino_modules}.items():
            if not (mod.name in self.broken_module_on_wait):
                try:
                    mod.on_wait()
                except Exception as e:
                    print("Exception found in module " + mod.name + " for on wait\n" + str(e.__doc__) + "\n" + str(e))
                    traceback.print_tb(e.__traceback__)
                    self.debug_run(print, mod.name + " removed from on_wait.")
                    self.broken_module_on_wait.append(mod.name)

    def _process_stdin(self):
        str_rsv = sys.stdin.readline()

        self.debug_run(print, "got message: " + str_rsv)

        try:
            self.local_modules.get(">").message_received(str_rsv)
        except Exception as e:
            print("Exception found in stdin module for message received --> "+str(e.__doc__)+"\n" + str(e))

    def _process_arduino_message(self, response):
        try:
            arduino_says = response.readline()
        except Exception as e:
            print(str(e))
            return

        message_from_arduino = arduino_says.decode("utf-8", 'ignore').strip()
        if message_from_arduino == "":
            self.debug_run(print, "Received empty message from arduino")
            return

        self.debug_run(print, "Messsage:" + message_from_arduino)

        module_to_use = self.arduino_modules.get(message_from_arduino.split(" ")[0].lower(), None)

        if module_to_use is not None:
            try:
                module_to_use.message_received(" ".join(message_from_arduino.split(" ")[1:]))
            except Exception as e:
                print("Exception found in module " + module_to_use.name + " for message received --> "+str(e.__doc__)+"\n" + str(e))
        else:
            self.debug_run(print, "Received incorrect module " + message_from_arduino.split(" ")[0])

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
        print(mod_name + ": " + msg)
        self.log_to_file(mod_name + ": " + msg)

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

    def __getitem__(self, item):
        return self.arduino_modules.get(item.strip().lower(), SamModule.SamModule())

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
    parser.add_argument("--run", nargs=1, type=str,
                        help="Run a file")
    parser.add_argument("--debug", action="store_true",
                        help="Run a file")

    args = parser.parse_args()

    sam = SamControl(args.log_file, args.arduino, args.debug)

    try:
        sam.main(program=args.run)
    except Exception as e:
        print("Sam has failed --> " + e.__doc__)
        print(str(e))
        print(e.with_traceback())
        sam.exit()

