from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
from detect_rgb4 import detect
import serial
import numpy as np
import os
import socket

port = '/dev/ttyACM0'
ser = serial.Serial(port, 115200, timeout=2)

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

X_RESOLUTION = 1280
Y_RESOLUTION = 960

# Initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (X_RESOLUTION, Y_RESOLUTION)
camera.framerate = 5
rawCapture = PiRGBArray(camera, size=(X_RESOLUTION, Y_RESOLUTION))

# Allow camera to warmup
time.sleep(0.1)
i = 0
previous = 0


#VelocityRight = (PWM+0.5181)/0.006
#VelocityLeft = (PWM+0.4988)/0.0058


def PWMToVelocity(leftPWM, rightPWM):

    return (leftPWM+10.974)/0.1278, (rightPWM+11.398)/0.1317

def speed(left, right):

    l, r = PWMToVelocity(left,right)

    motor_control = "m " + str(int(l)) + " " + str(int(r))
    #ser.write(motor_control.encode())
    #sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))


test = 0
folder = 'test/' + str(test)

if not os.path.isdir('test'):
    os.mkdir('test')

if not os.path.isdir(folder):
    os.mkdir(folder)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # Grab the raw NumPy array representing the image

    img = frame.array

    img = img[int(img.shape[0]/2):img.shape[0], :, :]
    #img = img[int(img.shape[0] / 3):img.shape[0] * 2 / 3, :, :]
    h, w, _ = img.shape

    key = cv2.waitKey(1) & 0xFF

    ml = mr = 15 #cm/s

    if i != 0:

        start = time.time()

        center, mid, command, ratio = detect(img)

        MESSAGE = "camera " + str(center) + " " +str(mid) + " " + str(command) + " " + str(ratio)+"\n"

        sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

        # center = 617 #620
        # diff = center - mid

        # #cv2.imwrite(folder + '/' + str(command) + '_' + str(ratio) + '.jpg', img)


        # # Tune pd: https://robotics.stackexchange.com/questions/167/what-are-good-strategies-for-tuning-pid-loops
        # # https://robotic-controls.com/learn/programming/pd-feedback-control-introduction

        # # Get there faster => Smaller Kp
        # # Less Overshoot => Smaller Kp, larger Kd
        # # Less Vibration => Larger Kd

        # # Kp => Increase to make larger corrections
        # # Kd => Increase to make damping greater
        # Kp = 0.01547 #0.01547
        # Kd = 0.0123  #0.0123

        # output = -(Kp * diff) - (Kd * (diff-previous))

        # if command == 'stop':
        #     print('Stop')
        #     speed(0, 0)
        #     #break


        # print("Output is: " + str(output))


        # speed(ml + output, mr - output)

        # # if output > 0:
        # #     speed(ml-output, mr+output)
        # # else:
        # #     speed(ml + output, mr - output)

        # previous = diff

        # end = time.time()


        # print('= = = = =')
        # print('frame: ' + str(i))
        # print([command, ratio])
        # print([center, mid, mid - center])
        # print(end - start)

    rawCapture.truncate(0)

    i = i + 1
