from .SamModule import SamModule
import time
import sys
import traceback
import serial.tools.list_ports


class StdinTools(SamModule):
    """
    Module for stdin functions. Not overly nessecary, but use this as a reference.
    """

    stdin_cmds = {}

    r1 = False
    r1_started = False
    r1_past_1 = False
    r1_starty = 0.0

    r2 = False
    r2_past_1 = False
    r2_starty = 0.0

    def __init__(self, kargs):
        super().__init__(module_name="StdinTools", is_local=True, identi=">", **kargs)

        self.stdin_cmds = {"modules": (lambda str_args: self.show_mods(),
                                       "View the modules"),
                           "set": (lambda str_args: self.set_var(str_args),
                                   "Use command to set certain SAM variables, such as 'set arduino /dev/usb000'"),
                           "request": (lambda str_args: self.request_module(str_args),
                                       "Use this command to talk to the modules. 'request <mod_name> txt'"),

                           "help": (lambda str_args: self.show_help(),
                                    "Use this command to see the help text"),

                           "h": (lambda str_args: self.show_help(),
                                 "Same as 'help'"),

                           "status": (lambda str_args: self.show_status(),
                                      "Get the status of the Arduino"),

                           "send": (lambda str_args: self.send_message(str_args),
                                    "Send a string to the arduino"),

                           "findarduino": (lambda str_args: self.find_arduino(),
                                           "Re-find the arduino"),

                           "debug": (lambda str_args: self.toggle_debug(str_args),
                                     "Change debugging to true or false"),

                           "wait": (lambda str_args: self.wait(str_args),
                                    "Change debugging to true or false"),

                           "run": (lambda str_args: self.run_file(str_args),
                                    "Run lines in a file"),

                           "echo": (lambda str_args: self.echo(str_args),
                                    "Echo a string"),

                           "quit": (lambda str_args: self.sam.request_quit(),
                                    "Quit the program"),

                           "r1": (lambda str_args: self.follow('r1'),
                                    "Start or stop r1"),

                           "r2": (lambda str_args: self.follow('r2'),
                                    "Start or stop r2"),

                           "exit": (lambda str_args: self.sam.request_quit(),
                                    "Same as quit")
                           }

    def message_received(self, message):
        if message.strip() == "":
            return

        message_arg = message.strip().split(" ")

        self.debug_run(print, "Function requested: " + message_arg[0])

        func_to_run, _ = self.stdin_cmds.get(message_arg[0], (None, None))

        if func_to_run is None:
            self.write_to_stdout("Cannot find command " + message_arg[0] + ". Use help to get help.")
        else:
            func_to_run(message_arg[1:])

    def find_arduino(self):
        self.sam.find_arduino()

    def toggle_debug(self, str_args):
        self.debug_run(print, "Toggling debugging, msg is " + str_args[0])
        if str_args[0].strip() == "true":
            self.sam.debug = True
        elif str_args[0].strip() == "false":
            self.sam.debug = False
        else:
            self.write_to_stdout("Cannot change debugging to " + str(str_args[0]))

    def show_mods(self):
        self.write_to_stdout(str([n for n in {**self.sam.arduino_modules, **self.sam.local_modules}.keys()]))

    def set_var(self, str_args):
        if len(str_args) == 2:
            if str_args[0].lower() == 'arduino':
                try:
                    serial.Serial(str_args[1], timeout=1, baudrate=115200)
                except Exception as e:
                    self.debug_run(self.write_to_stdout, "Could not connect to arduino: " + e.__doc__ + "\n" + str(e))
            else:
                self.write_to_stdout("Only setting arduino path is available")
        else:
            self.write_to_stdout("Need two arguments.")

        # TODO sam listening list is affected, fix is...

    def show_help(self):

        print("\n".join([cmd + " --> \n\t" + comment for cmd, (_, comment) in self.stdin_cmds.items()]))

    def show_status(self):
        to_print = "\n"

        if self.arduino is not None:
            to_print = to_print + "\tArduino is: " + self.sam.arduino.port + "\n"
        else:
            to_print = to_print + "\tArduino is not detected." + "\n"

        to_print = to_print + "\tDebugging is " + str(self.sam.debug) + "\n"

        to_print = to_print + "\tBroken modules: " + str(self.sam.broken_module_on_wait)

        self.write_to_stdout(to_print)

    def send_message(self, str_args):
        self.sam.send(" ".join(str_args))

    def request_module(self, str_args):

        get_mod = {**self.sam.arduino_modules, **self.sam.local_modules}.get(str_args[0])
        if get_mod is None:
            self.write_to_stdout("Cannot retrieve module named " + str_args[0])

        else:
            try:
                get_mod.stdin_request(" ".join(str_args[1:]))
            except Exception as e:
                self.write_to_stdout("Cannot run request for module " + get_mod.name + "\n" + str(e))
                traceback.print_tb(e.__traceback__)

    def wait(self, str_args):
        if len(str_args) > 0 and str_args[0].isdigit():
            time.sleep(int(str_args[0]))

    def echo(self, str_args):
        self.write_to_stdout(" ".join(str_args))

    def run_file(self, str_args):
        if str_args is None or len(str_args) < 1 or str_args[0].strip() == "":
            self.write_to_stdout("Cannot open file")
            return

        to_run = open(str_args[0], 'r', encoding='utf-8')

        line_to_read = to_run.readline()
        while line_to_read is not "":

            if line_to_read.strip() != "":
                # Ignore empty lines
                self.message_received(line_to_read.strip())
                # Keeps file reading from being non-blocking
                self.sam.process_sockets()

            line_to_read = to_run.readline()

    def follow(self, routine):
        if routine == 'r1':
            self.r1 = not self.r1
            if self.r1:
                self.sam['camera'].stdin_request('start')
                self.write_to_stdout("starting r1")
            else:
                self.sam['camera'].stdin_request('stop')
                self.sam['motor'].stdin_request('stop')
        elif routine == 'r2':
            self.r2 = not self.r2
            if self.r2:
                self.sam['camera'].stdin_request('start')
                self.write_to_stdout("starting r2")
            else:
                self.sam['camera'].stdin_request('stop')
                self.sam['motor'].stdin_request('stop')

    def on_wait(self):
        # self.debug_run(self.write_to_stdout, "starting ir")
        x, y, h = self.sam['ir'].current_location
        # self.debug_run(self.write_to_stdout, "in ir")
        if x is None:
            self.write_to_stdout("cannot get ir module")

        if self.r1:
            if x >= 20.5:
                if not self.r1_past_1:
                    self.debug_run(self.write_to_stdout, "in turn")
                    self.sam['camera'].stdin_request('stop')
                    self.r1_starty = y
                    self.sam['motor'].done = False
                    self.sam['motor'].send('y')
                    self.r1_past_1 = True
                elif self.sam['motor'].done:
                    if not self.sam['camera'].is_following_lane:
                        self.r1_starty = y
                        self.sam['camera'].stdin_request('start')
                    else:
                        if (y-self.r1_starty) >= 42.5:
                            self.follow('r1')
                            self.write_to_stdout("ending r1")

        elif self.r2:
            # self.debug_run(self.write_to_stdout, "in r1")
            if x > 43:
                if not self.r2_past_1:
                    self.debug_run(self.write_to_stdout, "in turn")
                    self.sam['camera'].stdin_request('stop')
                    self.r2_starty = y
                    self.sam['motor'].done = False
                    self.sam['motor'].send('x')
                    self.r2_past_1 = True
                elif self.sam['motor'].done:
                    if not self.sam['camera'].is_following_lane:
                        self.r2_starty = y
                        self.sam['camera'].stdin_request('start')
                    else:
                        if (y-self.r2_starty) <= -17.5:
                            self.follow('r2')
                            self.write_to_stdout("ending r2")


