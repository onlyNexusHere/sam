from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
from detect_rgb2 import detect
import serial
import numpy as np


port = '/dev/ttyACM0'
ser = serial.Serial(port, 115200, timeout=2)

X_RESOLUTION = 1280
Y_RESOLUTION = 960

# Initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (X_RESOLUTION, Y_RESOLUTION)
camera.framerate = 10
rawCapture = PiRGBArray(camera, size=(X_RESOLUTION, Y_RESOLUTION))

# Allow camera to warmup
time.sleep(0.1)
i = 0

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # Grab the raw NumPy array representing the image
    time.sleep(5)
    img = frame.array
    cv2.imwrite('polar_img/path_' + str(i) + '.png', img)
    rawCapture.truncate(0)
    print('took frame ', i)
    i += 1
    if i == 9:
        break
