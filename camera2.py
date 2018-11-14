import time
import picamera
from PIL import Image,ImageDraw

with picamera.PiCamera() as camera:
    camera.resolution = (1024, 768)
    camera.start_preview()
    time.sleep(2)
    curr = time.time()


    last_adjustment = 0
    adjustment = 0
    # Tune these 
    K = 3
    B = 1
    m1speed = 160
    m2speed = 160

    motor_command = str(m1speed) + ' ' + str(m2speed)
    # self.sam['motor'].send(motor_command)
    while(True):
        # Camera warm-up time
        
        # img = camera.capture('foo.jpg')
        #print("Picture Taken")
        img = Image.open('a.jpg').convert('LA')
        pix = img.load()
        #print("Time Elapsed",curr-time.time())
        curr = time.time()
        threshold = 200
        thresholdy = 200
        w, h = img.size
        
        middle = 190
        middley = 33
        for item in range(int(w/2),0,-1):

            if(pix[item,int(h*.35)][0]>threshold):
                break
        for itemy in range(0,int(w/2),1):

            if(pix[itemy,int(h*.35)][0]>thresholdy):
                break
        adjustment = item - middle
        adjustmenty = itemy - middley
        # print(adjustment)
        # based on the project 3 notes on the table next to the track
        errorDD = -K*adjustment-B*(adjustment-last_adjustment)
        m1speed = m1speed + errorDD
        m2speed = m2speed - errorDD
        motor_command = str(m1speed) + ' ' + str(m2speed)
        # self.sam['motor'].send(motor_command)
