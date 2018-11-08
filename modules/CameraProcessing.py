import sys

import select
import serial.tools.list_ports
import datetime

from .SamModule import SamModule

class CameraProcessing(SamModule):
    def __init__(self, kargs):
        super().__init__(module_name="CameraProcessing", is_local=True, identi="camera", **kargs)

        # Here: add the thing to upload an image


    def stdin_request(self, message):
        pass

    def on_wait(self):
        # Read camera?

        # camera_say is list split by " "
        camera_says = None
        if camera_says is not None:
            if camera_says[0] == "r":
                if len(camera_says) > 1:
                    self.sam.motors.send("turn right " + camera_says[1])


    def write_to_stdout(self, string_to_write):
        pass

    def log_to_file(self, string_to_log):
        pass

