from .SamModule import SamModule

from datetime import datetime, timedelta

class Motors(SamModule):
    """
    Module for motor functions.
    """

    stdin_cmds = {}

    #send in some amount time, (exact_time, message)
    promise = []
    ready = True

    def __init__(self, kargs):
        super().__init__(module_name="Motors", is_local=False, identi="motor", **kargs)

    def message_received(self, message):
        pass

    def stdin_request(self, message):
        """
        Request the motors to do something, for example:

        motor turn right
        motor turn left
        motor straight
        motor wait 2 straight

        :param message:
        :return:
        """

        message_parts = message.strip().split(" ")

        self.debug_run(self.write_to_stdout, "Processing motor command " + message + " \n Command is: " + message_parts[0])

        if message_parts is None or len(message_parts) == 0:
            self.write_to_stdout("Cannot send empty message to arduino: " + message)
            return

        if message_parts[0].lower() == "turn":

            if len(message_parts) < 2:
                self.write_to_stdout("Need direction to turn")
                return
            elif message_parts[1].lower() == "right":
                self.send("turn right")

            elif message_parts[1].lower() == "left":
                self.send("turn left")

            else:
                self.write_to_stdout("Cannot turn " + message_parts[1].lower())

        elif message_parts[0].lower() == "adjust":

            if len(message_parts)<2:
                self.write_to_stdout("Need direction to turn")
                return

            elif message_parts[1].lower() == "right":
                self.send("adjust right")

            elif message_parts[1].lower() == "left":
                self.send("adjust left")

            else:
                self.write_to_stdout("Cannot turn " + message_parts[1].lower())

        elif message_parts[0].lower() == "stop":
            self.send("0 0 0")

        elif message_parts[0].lower() == "start" or message_parts[0].lower() == "straight":
            self.debug_run(self.write_to_stdout, "Sending straight")
            self.send("1 200 200")

        elif message_parts[0] == "wait" and len(message_parts) > 2:
            if not message_parts[1].isdigit():
                if self.sam.debug: self.write_to_stdout("Cannot wait for non-digit seconds")

            seconds = int(message_parts[1])
            command = " ".join(message_parts[2:])

            now = datetime.now()
            future = now + timedelta(seconds=seconds)
            self.debug_run(self.write_to_stdout, "In " + str(seconds) + " seconds " + command + " will run.")
            self.promise.append((future, command))

        elif len(message_parts) > 2 and message_parts[0] == 'then':
            if len(self.promise) > 0:
                next_time, cmd = self.promise[-1]

                new_time = next_time + timedelta(milliseconds=100)

                self.promise.append((new_time, " ".join(message_parts[1:])))

    def on_wait(self):

        now = datetime.now()
        to_delete = []

        for time, cmd in self.promise:
            if time <= now:
                to_delete.append((time, cmd))
                self.stdin_request(cmd)

        for time, cmd in to_delete:
            self.promise.remove((time, cmd))

        self.ready = len(self.promise) < 1



