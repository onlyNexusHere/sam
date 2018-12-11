from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
from detect_rgb3 import detect
import serial
import numpy as np
import os


port = '/dev/ttyACM0'
ser = serial.Serial(port, 250000, timeout=2)

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


def speed(left, right):
    motor_control = "m " + str(int(left)) + " " + str(int(right))
    ser.write(motor_control.encode())


test = 0
folder = 'test_' + str(test)
if not os.path.isdir(folder):
    os.mkdir(folder)

for frame in camera.capture_continuous(rawCapture, format="rgb", use_video_port=True):
    # Grab the raw NumPy array representing the image

    img = frame.array
    key = cv2.waitKey(1) & 0xFF

    # cv2.imwrite('0.png', img)

    # Clear the stream so it is ready to receive the next frame
    rawCapture.truncate(0)

    if i != 0:
        print('= = = = =')
        print('frame: ' + str(i))

        s = time.time()

        center, mid, command, ratio = detect(img)

        print(time.time() - s)

        print(command, ratio)
        print([center, mid])

        sta = [command, ratio, center, mid]
        # cv2.imwrite(folder + '/' + str(i) + '_' + str(sta) + '.png', img[int(img.shape[0] / 2):int(img.shape[0]), :, :])

        ml = mr = 180

        diff = center - mid

        rat = np.abs(diff) / (center / 2)

        stay = 100

        if command == 'stop':
            print('Stop')
            speed(0, 0)

        if np.abs(diff) <= stay:
            if np.abs(diff) > 15:
                if diff > 0:
                    print('leftttttttttttt')
                    speed(ml - np.abs(diff) * 0.1, mr + np.abs(diff) * 0.1)
                else:
                    print('righttttttttttt')
                    speed(ml + np.abs(diff) * 0.1, mr - np.abs(diff) * 0.1)
            else:
                print('Stay on center')
                speed(ml, mr)



        # if np.abs(diff) <= stay:
        #     if diff > 0:
        #         print('leftttttttttttt')
        #         speed(ml - diff * 0.5, mr + diff * 0.5)
        #     else:
        #         print('righttttttttttt')
        #         speed(ml + diff * 0.5, mr - diff * 0.5)



        elif diff > stay:
            print('Turn left')
            speed(ml - 70, mr + 25)

        elif diff < -stay:
            print('Turn right')
            speed(ml + 25, mr - 70)

    i += 1




    # if command == 'straight':
    #
    #     if 0 < center < mid[1] - 160 * 2:
    #         motor_control = "m 151 150"
    #         ser.write(motor_control.encode())
    #     elif mid[1] + 160 * 2 < center < mid[1] * 2:
    #         motor_control = "m 150 151"
    #         ser.write(motor_control.encode())
    #     else:
    #         motor_control = "m 150 150"
    #         ser.write(motor_control.encode())
    #
    # elif command == 'turn left':
    #     print(":" + command + ":")
    #     motor_control = "m 0 0"
    #     ser.write(motor_control.encode())
    #     break
    #
    # elif command == 'turn right':
    #     print(":" + command + ":")
    #     motor_control = "m 0 0"
    #     ser.write(motor_control.encode())
    #     break
    #
    # else:
    #     break
    #     print(":" + command + ":")
    #     motor_control = "m 0 0"
    #     ser.write(motor_control.encode())

    # if i == 30:
    #     break

    # i += 1

# print(yellow)
# print(white)

