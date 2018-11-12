import sys

import select
import serial.tools.list_ports
import datetime

from picamera import PiCamera
import serial
import time
import numpy as np
from PIL import Image
from pi.detect_1 import detect_mid


from .SamModule import SamModule

class CameraProcessing(SamModule):
    ml = 0
    mr = 0
    path = None
    prev = None
    camera = None

    is_following_lane = False

    def __init__(self, kargs):
        super().__init__(module_name="CameraProcessing", is_local=True, identi="camera", **kargs)

        # Here: add the thing to upload an image


        self.camera = PiCamera()

        self.camera.start_preview()

        self.path = '/home/pi/Desktop/503/path.jpg'

        self.is_following_lane = False

    def stdin_request(self, message):
        if message.strip() == "start":
            self.is_following_lane = True
            self.ml = 120
            self.mr = 125
            motor_command = str(self.ml) + ' ' + str(self.mr)
            self.sam['motor'].send(motor_command.encode('utf-8'))
            self.prev = 640/2

        elif message.strip() == "stop":
            self.is_following_lane = False

    def on_wait(self):

        if self.is_following_lane:

            start = time.time()
            self.camera.capture(self.path)
            img = np.array(Image.open(self.path).convert('L'))
            mid = detect_mid(img)[0]
            process_time = detect_mid(img)[1]
            print('= = = = = = =')
            end = time.time()
            print('Process Time: ' + str(process_time))
            print('Total Time: ' + str(end - start))
            print('Mid: ' + mid)
            if mid > self.prev:
                motor_command = str(1.2 * self.ml) + ' ' + str(self.mr)
                self.sam['motor'].send(motor_command.encode())
            else:
                motor_command = str(self.ml) + ' ' + str(1.2 * self.mr)
                self.sam['motor'].send(motor_command.encode())
            self.prev = mid

    def write_to_stdout(self, string_to_write):
        pass

    def log_to_file(self, string_to_log):
        pass

    def exit(self):
        self.camera.stop_preview()
