from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.resolution = (1920, 1440)
camera.start_preview()
for i in range(18):
    camera.capture('/home/sam_student/sam/pi/test_img2/path_' + str(i) + '.jpg')
    print('took path_' + str(i))
    sleep(7)
camera.stop_preview()