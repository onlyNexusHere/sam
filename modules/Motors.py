from .SamModule import SamModule


class Motors(SamModule):
    """
    Module for motor functions.
    """

    stdin_cmds = {}

    def __init__(self, kargs):
        super().__init__(module_name="Motors", is_local=False, identi="motor", **kargs)

    def message_received(self, message):
        pass

    def stdin_request(self, message):

        message_parts = message.strip().split(" ")

        if message_parts is None:
            self.write_to_stdout("Cannot send empty message to arduino: " + message)
            return

        if message_parts[0].lower() == "turn":
            if len(message_parts)<2:
                self.write_to_stdout("Need direction to turn")
                return
            elif message_parts[1].lower() == "right":
                self.send("motor turn right")
            elif message_parts[1].lower() == "left":
                self.send("motor turn left")
            else:
                self.write_to_stdout("Cannot turn " + message_parts[1].lower())

        if message_parts[0].lower() == "adjust":
            if len(message_parts)<2:
                self.write_to_stdout("Need direction to turn")
                return
            elif message_parts[1].lower() == "right":
                self.send("motor adjust right")
            elif message_parts[1].lower() == "left":
                self.send("motor adjust left")
            else:
                self.write_to_stdout("Cannot turn " + message_parts[1].lower())

        if message_parts[0].lower() == "stop":
            self.send("motor stop")

        if message_parts[0].lower() == "start":
            self.send("motor start")