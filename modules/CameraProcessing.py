import sys

import select
import serial.tools.list_ports
import datetime

from .SamModule import SamModule

import os.path

if os.path.isfile("/proc/cpuinfo"):
    import picamera
else:
    picamera = None

class CameraProcessing(SamModule):
    def __init__(self, kargs):
        super().__init__(module_name="CameraProcessing", is_local=True, identi="camera", **kargs)

        # Here: add the thing to upload an image


    def stdin_request(self, message):
        if message == "process":
            pass

    def on_wait(self):
        pass

    def write_to_stdout(self, string_to_write):
        pass

    def log_to_file(self, string_to_log):
        pass

