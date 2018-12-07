import sys
import socket

from .SamModule import SamModule



class CameraProcessing(SamModule):

    def __init__(self, kargs):
        super().__init__(module_name="CameraProcessing", is_local=True, identi="camera", **kargs)

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('127.0.0.1', 5005))
        self.sam.listening_to[sock] = self.message_received

    def stdin_request(self, message):
        pass

    def message_received(self, message):
       pass

    def write_to_stdout(self, string_to_write):
        pass

    def log_to_file(self, string_to_log):
        pass

    def exit(self):
        pass
