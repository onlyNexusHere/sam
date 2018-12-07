from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
from detect_rgb import detect


X_RESOLUTION = 1280
Y_RESOLUTION = 960

# Initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (X_RESOLUTION, Y_RESOLUTION)
camera.framerate = 10
rawCapture = PiRGBArray(camera, size = (X_RESOLUTION, Y_RESOLUTION))

# camera.start_preview()

# Allow camera to warmup
time.sleep(0.1)
i = 0
#Capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # Grab the raw NumPy array representing the image
    start = time.time()
    img = frame.array
    print('= = = = =')
    print("Frame ", i)
    # print(image.shape)
    # cv2.imwrite('./cv2.jpg', image)
    # Show the frame
    #cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF
    i+=1
    # Clear the stream so it is ready to receive the next frame
    rawCapture.truncate(0)
    mid, command = detect(img)
    end = time.time()
    # print(midmid)
    print(command)
    print(end - start)
    time.sleep(5)
    # If the 'q' key was pressed, break from the loop
    if i == 3000:
        camera.close()
