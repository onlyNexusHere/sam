// This has been destroyed by merges, but will remain here for reference.

import time
import picamera
from PIL import Image,ImageDraw

with picamera.PiCamera() as camera:
    camera.resolution = (1024, 768)
    camera.start_preview()
    time.sleep(2)
    curr = time.time()

    while(True):
    	# Camera warm-up time
        
    	img = camera.capture('foo.jpg')
	#print("Picture Taken")
	img = Image.open('foo.jpg').convert('LA')
	pix = img.load()
	#print("Time Elapsed",curr-time.time())
	curr = time.time()
	threshold = 200
	w, h = img.size
	
	middle=218
	for item in range(int(w/2),0,-1):

		if(pix[item,int(h*.4)][0]>threshold):
			#print(item)
			#if(item>middle):
			#print("Camera l ", abs(item-203))

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
        
        img = camera.capture('foo.jpg')
        #print("Picture Taken")
        img = Image.open('foo.jpg').convert('LA')
        pix = img.load()
        #print("Time Elapsed",curr-time.time())
        curr = time.time()
        threshold = 200
        w, h = img.size
        
        middle=86
        for item in range(int(w/2),0,-1):


            if(pix[item,int(h*.35)][0]>threshold):
                break
        adjustment = item-middle
        print(adjustment)
        # based on the project 3 notes on the table next to the track
        errorDD = -K*adjustment-B*(adjustment-last_adjustment)
        m1speed = m1speed + errorDD
        m2speed = m2speed - errorDD
        motor_command = str(m1speed) + ' ' + str(m2speed)
        # self.sam['motor'].send(motor_command)

	adjustment = item-middle
	print("item: ",item)
	print("adjustment: ",adjustment)
	

