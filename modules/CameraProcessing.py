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

class CameraProcessing:
    def __init__(self, **kargs):
        super().__init__("CameraProcessing", is_local=True, identi="camera", **kargs)

        # Here: add the thing to upload an image


    def stdin_request(self, message):
        if message == "process":
            pass

    def on_wait(self):
        # with picamera.PiCamera() as camera:
        #     camera.resolution = (1024, 768)
        #     camera.start_preview()

        pass

    def write_to_stdout(self, string_to_write):
        pass

    def log_to_file(self, string_to_log):
        pass

