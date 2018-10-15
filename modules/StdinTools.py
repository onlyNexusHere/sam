
from .SamModule import SamModule


class StdinTools(SamModule):
    """
    Module for stdin functions. Not overly nessecary, but use this as a reference.
    """

    stdin_cmds = {}


    def __init__(self, **kargs):
        super().__init__("StdinTools", is_local=True, identi=">", **kargs)

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
                           "quit": (lambda str_args: self.sam.request_quit(),
                                    "Quit the program")
                           }

    def run(self, message: str):
        message_arg = message.strip().split(" ")
        print("Function requested: " + message_arg[0])

        func_to_run, _ = self.stdin_cmds.get(message_arg[0], (None, None))

        if func_to_run is None:
            self.write_to_stdout("Cannot find command " + message_arg[0] + ". Use help to get help.")
        else:
            func_to_run(message_arg[1:])

    def show_mods(self):
        self.write_to_stdout(str([n for n in {**self.sam.arduino_modules, **self.sam.local_modules}.keys()]))

    def set_var(self, message: list):
        pass

    def show_help(self):

        print("\n".join([cmd + " --> \n\t" + comment for cmd, (_, comment) in self.stdin_cmds.items()]))

    def request_module(self, str_args):

        get_mod: SamModule = {**self.sam.arduino_modules, **self.sam.local_modules}.get(str_args[0])
        if get_mod is None:
            self.write_to_stdout("Cannot retrieve module named " + str_args[0])

        else:
            get_mod.stdin_request(" ".join(str_args[1:]))


