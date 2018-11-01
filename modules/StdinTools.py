
from .SamModule import SamModule


class StdinTools(SamModule):
    """
    Module for stdin functions. Not overly nessecary, but use this as a reference.
    """

    stdin_cmds = {}

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

                           "quit": (lambda str_args: self.sam.request_quit(),
                                    "Quit the program")
                           }

    def message_received(self, message):
        message_arg = message.strip().split(" ")
        print("Function requested: " + message_arg[0])

        func_to_run, _ = self.stdin_cmds.get(message_arg[0], (None, None))

        if func_to_run is None:
            self.write_to_stdout("Cannot find command " + message_arg[0] + ". Use help to get help.")
        else:
            func_to_run(message_arg[1:])

    def find_arduino(self):
        self.sam.find_arduino()

    def toggle_debug(self, msg):
        if self.sam.debug: print("Toggling debugging, msg is " + msg[0])
        if msg[0].strip() == "true":
            self.sam.debug = True
        elif msg[0].strip() == "false":
            self.sam.debug = False
        else:
            self.write_to_stdout("Cannot change debugging to "+str(msg[0]))

    def show_mods(self):
        self.write_to_stdout(str([n for n in {**self.sam.arduino_modules, **self.sam.local_modules}.keys()]))

    def set_var(self, message: list):
        pass

    def show_help(self):

        print("\n".join([cmd + " --> \n\t" + comment for cmd, (_, comment) in self.stdin_cmds.items()]))

    def show_status(self):

        if self.sam.arduino is not None:
            self.write_to_stdout("Arduino is: " + self.sam.arduino.port + "\nDebugging is " + str(self.sam.debug))
        else:
            self.write_to_stdout("Arduino is not detected.")

    def send_message(self, message):
        self.sam.send(message)

    def request_module(self, str_args):

        get_mod = {**self.sam.arduino_modules, **self.sam.local_modules}.get(str_args[0])
        if get_mod is None:
            self.write_to_stdout("Cannot retrieve module named " + str_args[0])

        else:
            get_mod.stdin_request(" ".join(str_args[1:]))


