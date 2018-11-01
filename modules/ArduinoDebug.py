from .SamModule import SamModule


class ArduinoDebug(SamModule):
    """
    Module for stdin functions. Not overly nessecary, but use this as a reference.
    """

    stdin_cmds = {}
    debug = None

    def __init__(self, **kargs):
        super().__init__("ArduinoDebug", is_local=False, identi="Debug", **kargs)
        self.debug = kargs.get("debug")

    def message_received(self, message):
        if self.debug: self.write_to_stdout(message)
