from picamera import PiCamera
import serial
import time
import numpy as np
from PIL import Image
from detect_1 import detect_mid


def main():

    port = '/dev/cu.usbmodem14101'
    ser = serial.Serial(port, 9600, timeout=2)

    ml = 120
    mr = 125

    motor_command = str(ml) + ' ' + str(mr)
    ser.write(motor_command.encode())

    camera = PiCamera()
    # camera.color_effects = (128, 128)
    # camera.framerate = 10
    camera.start_preview()

    path = '/home/pi/Desktop/503/path.jpg'

    prev = 640 / 2

    while True:

        start = time.time()
        camera.capture(path)
        img = np.array(Image.open(path).convert('L'))
        mid = detect_mid(img)[0]
        process_time = detect_mid(img)[1]
        print('= = = = = = =')
        end = time.time()
        print('Process Time: ' + str(process_time))
        print('Total Time: ' + str(end - start))
        print('Mid: ' + mid)
        if mid > prev:
            motor_command = str(1.2 * ml) + ' ' + str(mr)
            ser.write(motor_command.encode())
        else:
            motor_command = str(ml) + ' ' + str(1.2 * mr)
            ser.write(motor_command.encode())
        prev = mid

        time.sleep(0.5)

    camera.capture(path)

    camera.stop_preview()


main()
