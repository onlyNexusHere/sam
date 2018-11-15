from .SamModule import SamModule


class Quadrature(SamModule):
    """
    Module for ir functions.
    """

    current_location = (None, None, None)
    waiting_for_location = False

    def __init__(self, kargs):
        super().__init__(module_name="Quadrature", is_local=False, identi="ir", **kargs)
        self.current_location = (float(0), float(0), float(0))
        self.send_id = "i"

    def message_received(self, message):
        """
        There only information sent from the arduino will be "ir x y heading"

        :param message:
        :return:
        """
        self.debug_run(self.write_to_stdout, "Got IR message")
        msg_parts = message.strip().split(" ")

        # 0 will be x, 1 will be y, 2 will be heading.

        if len(msg_parts) < 3:
            self.debug_run(self.write_to_stdout, "Received packets that cannot be read")
        else:
            try:
                x = float(msg_parts[0])
                y = float(msg_parts[1])
                heading = float(msg_parts[2])

                self.current_location = (x, y, heading)

                if self.waiting_for_location:
                    # If the location was requested to print out the location, print it.
                    self.write_to_stdout("Current location is " + str(x) + " " + str(y) + " " + str(heading))
                    self.waiting_for_location = False

            except ValueError:
                self.debug_run(self.write_to_stdout, "Cannot process message that is not 3 floats.")

    def stdin_request(self, message):
        if message.strip() == "get location" or message.strip() == "location" or message.strip() == "get":
            # self.send(" ")
            self.waiting_for_location = True
            # Next time a packet is received, the location will be printed

        elif message.strip() == "reset":
            self.send("reset")

    def on_wait(self):
        # We always want to get updates about the location of robot.
        # self.send(" ")
        pass




