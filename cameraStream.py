from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
MESSAGE = ""

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

X_RESOLUTION = 640
Y_RESOLUTION = 480

# Initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (X_RESOLUTION, Y_RESOLUTION)
camera.framerate = 10
rawCapture = PiRGBArray(camera, size = (X_RESOLUTION, Y_RESOLUTION))

camera.start_preview()

# Allow camera to warmup
time.sleep(0.1)
i = 0
#Capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # Grab the raw NumPy array representing the image
    image = frame.array

    # Show the frame
    #cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF
    print("Frame ",i) 
    i+=1

    sock.sendto("WAZUP", (UDP_IP, UDP_PORT))
    # Clear the stream so it is ready to receive the next frame
    rawCapture.truncate(0)

    # If the 'q' key was pressed, break from the loop
    if(key == ord('q')):
        camera.stop_preview()
        break
