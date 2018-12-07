from .SamModule import SamModule


class Ping(SamModule):
    """
    Module for ping functions.
    """

    stdin_cmds = {}

    def __init__(self, kargs):
        super().__init__(module_name="Ping", is_local=False, identi="ping", **kargs)
        self.prev_dist = 100
        self.send_id = "p"

    def message_received(self, message):
        dist = int(message)
        # if dist > 24:
        #     # it's far away
        #     return
        # elif dist < 6:
        #     # oh shit
        #     self.sam['motor'].stop()
        # else:
        #     if prev_dist <= dist:  # it's getting farther
        #         return
        #     elif prev_dist > dist: # it's getting closer
        #         self.sam['motor'].slow(10, 10)
        print(dist)

    def on_wait(self):
        self.send(" ")

