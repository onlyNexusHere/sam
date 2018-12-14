from .SamModule import SamModule


class Ping(SamModule):
    """
    Module for ping functions.
    """

    stdin_cmds = {}

    def __init__(self, kargs):
        super().__init__(module_name="Ping", is_local=False, identi="ping", **kargs)
        self.last = -1.0
        self.send_id = "p"

    def message_received(self, message):
        self.debug_run(self.write_to_stdout, "ping message received")

        # 0 will be x, 1 will be y, 2 will be heading.

        if len(msg_parts) < 1:
            self.debug_run(self.write_to_stdout, "Received packets that cannot be read")
        else:
            try:
                self.last = float(message)

            except ValueError:
                self.debug_run(self.write_to_stdout, "Cannot process message that is not 1 float.")
