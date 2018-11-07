from .SamModule import SamModule


class Ping(SamModule):
    """
    Module for ping functions.
    """

    stdin_cmds = {}

    def __init__(self, kargs):
        super().__init__(module_name="Ping", is_local=False, identi="ping", **kargs)

    def message_received(self, message):
        pass
