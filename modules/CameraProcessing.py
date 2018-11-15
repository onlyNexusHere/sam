import sys

import select
import serial.tools.list_ports
import datetime

from picamera import PiCamera
import serial
import time
import numpy as np
from PIL import Image

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


        self.path = '/home/sam_student/vision2/sam/foo.jpg'

        self.is_following_lane = False


    def stdin_request(self, message):

        if message.strip() == "start":
            self.is_following_lane = True
            self.ml = 160
            self.mr = 160
            motor_command = str(self.ml) + ' ' + str(self.mr)
            self.sam['motor'].send(motor_command)
            self.prev = 0
            self.K = 1/2000.0
            self.B = 1/4000.0

        elif message.strip() == "stop":
            self.is_following_lane = False
            self.sam['motor'].send("0 0 0")

    def on_wait(self):

        # Check for if obstacle
        # Check for intersection
        # Check for middle of lane

        if self.is_following_lane:

            start = time.time()
            self.camera.capture(self.path)
            #import pdb; pdb.set_trace()
            img = Image.open('foo.jpg').convert('LA')
            pix = img.load()
            threshold = 200
            thresholdy = 100
            w, h = img.size
            
            middle = 140
            middley = 800
            for item in range(int(w/2),0,-1):
                if(pix[item,int(h*.35)][0]>threshold):
                    break
            for itemy in range(int(w/2),w,1):
                if(pix[itemy,int(h*.35)][0]>thresholdy):
                    break
            adjustmentw = item - middle #changed
            adjustmenty = itemy - middley 

            if item == 1 and itemy == 1023:
                # well shit
                adjustment = 0
                pass
            elif item == 1 and itemy != 1023:
                adjustment = adjustmenty
            elif item != 1 and itemy == 1023:
                adjustment = adjustmentw
            else:
                adjustment = (adjustmenty + adjustmentw) / 2

            errorDD = -self.K*adjustment-self.B*(adjustment-self.prev)
            self.debug_run(self.write_to_stdout, "eDD: {}".format(errorDD))
            self.debug_run(self.write_to_stdout, "adjustment: {}".format(adjustment))
            self.debug_run(self.write_to_stdout, "adjustmentw: {}".format(adjustmentw))
            self.debug_run(self.write_to_stdout, "adjustmenty: {}".format(adjustmenty))
            self.debug_run(self.write_to_stdout, "itemw: {}".format(item))
            self.debug_run(self.write_to_stdout, "itemy: {}".format(itemy))


            self.ml = int(self.ml + errorDD)
            self.mr = int(self.mr - errorDD)
            motor_command = str(self.ml) + ' ' + str(self.mr)
            self.sam['motor'].send(motor_command)
            self.prev = adjustment


    def adjust_to_straight(self):

        start = time.time()
        self.camera.capture(self.path)
        img = np.array(Image.open(self.path).convert('L'))
        mid = detect_mid(img)
        # process_time = detect_mid(img)[1]
        self.debug_run(self.write_to_stdout,'= = = = = = =')
        end = time.time()
        # print('Process Time: ' + str(process_time))
        self.debug_run(self.write_to_stdout, 'Total Time: ' + str(end - start))
        self.debug_run(self.write_to_stdout, 'Mid: ' + str(mid))
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
