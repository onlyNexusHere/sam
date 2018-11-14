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

        self.path = '/home/sam_student/sam/path.jpg'

        self.is_following_lane = False


    def stdin_request(self, message):

        if message.strip() == "start":
            self.is_following_lane = True
            self.ml = 160
            self.mr = 160
            motor_command = str(self.ml) + ' ' + str(self.mr)
            self.sam['motor'].send(motor_command)
            self.prev = 0
            self.K = 2
            self.B = 2

        elif message.strip() == "stop":
            self.is_following_lane = False

    def on_wait(self):

        # Check for if obstacle
        # Check for intersection
        # Check for middle of lane

        if self.is_following_lane:

            start = time.time()
            self.camera.capture(self.path)
            img = np.array(Image.open(self.path).convert('L'))
            mid = detect_mid(img)

            # process_time = detect_mid(img)[1]
            # print('= = = = = = =')
            # end = time.time()
            # print('Process Time: ' + str(process_time))
            # print('Total Time: ' + str(end - start))
            # print('Mid: ' + str(mid))
            # if mid > self.prev:
            #     motor_command = str(1.2 * self.ml) + ' ' + str(self.mr)
            #     self.sam['motor'].send(motor_command)
            # else:
            #     motor_command = str(self.ml) + ' ' + str(1.2 * self.mr)
            #     self.sam['motor'].send(motor_command)
            # self.prev = mid
            errorDD = -K*adjustment-B*(adjustment-self.prev)
            self.ml = self.ml + errorDD
            self.mr = self.mr - errorDD
            motor_command = str(self.ml) + ' ' + str(self.mr)
            self.sam['motor'].send(motor_command)
            self.prev = adjustment


    def adjust_to_straight(self):

        start = time.time()
        self.camera.capture(self.path)
        img = np.array(Image.open(self.path).convert('L'))
        mid = detect_mid(img)
        # process_time = detect_mid(img)[1]
        print('= = = = = = =')
        end = time.time()
        # print('Process Time: ' + str(process_time))
        print('Total Time: ' + str(end - start))
        print('Mid: ' + str(mid))
        if mid > self.prev:
            motor_command = str(1.2 * self.ml) + ' ' + str(self.mr)
            self.sam['motor'].send(motor_command)
        else:
            motor_command = str(self.ml) + ' ' + str(1.2 * self.mr)
            self.sam['motor'].send(motor_command)
        self.prev = mid

    def check_for_intersection(self):
        # If there an intersection??
        pass

    def check_for_obsticle(self):
        # Is there an obstacle??
        pass

    def check_for_end(self):
        # Have we reached the edge of the map??
        pass

    def write_to_stdout(self, string_to_write):
        pass

    def log_to_file(self, string_to_log):
        pass

    def exit(self):
        self.camera.stop_preview()
