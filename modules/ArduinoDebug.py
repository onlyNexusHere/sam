from .SamModule import SamModule


class ArduinoDebug(SamModule):
    """
    Module for stdin functions. Not overly nessecary, but use this as a reference.
    """

    stdin_cmds = {}
    debug = None

    def __init__(self, kargs):
        super().__init__(module_name="ArduinoDebug", is_local=False, identi="Debug", **kargs)

    def message_received(self, message):
        self.debug_run(print, "debug mod")
        self.debug_run(self.write_to_stdout, message)
        # self.write_to_stdout(message)

