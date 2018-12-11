import sys
import socket

from .SamModule import SamModule

class CameraProcessing(SamModule):

    is_following_lane = False

    def __init__(self, kargs):
        super().__init__(module_name="CameraProcessing", is_local=True, identi="camera", **kargs)

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('127.0.0.1', 5005))
        self.sam.listening_to[sock] = self._process_socket

    def _process_socket(self, soc):
        data = soc.recv(1024)
        if data:
            self.message_received(data.decode("utf-8", 'ignore').strip())

    def stdin_request(self, message):
        if message == "go":
            self.is_following_lane = True

        elif message == "stop":
            self.is_following_lane = False

    def message_received(self, message):
        msg_parts = message.strip().split(" ")
        s_1 = 0
        s_2 = 0
        if len(msg_parts) != 2:
            self.debug_run(self.write_to_stdout, "Need exactly two numbers")
            return
        try:
            s_1 = int(msg_parts[0])
            s_2 = int(msg_parts[1])
        except ValueError:
            self.debug_run(self.write_to_stdout, "Need numbers")
            return

        if self.is_following_lane:
            self.sam['motor'].stdin_request("turn " + str(self.sam['motor'].current_speed[0] + s_1) + " " + str(self.sam['motor'].current_speed[1] + s_2))
            self.debug_run(self.write_to_stdout, "change:" + message)

    def write_to_stdout(self, string_to_write):
        pass

    def log_to_file(self, string_to_log):
        pass

    def exit(self):
        pass
