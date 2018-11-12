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
	print("Picture Taken")
	img = Image.open('foo.jpg').convert('LA')
	pix = img.load()
	print("Time Elapsed",curr-time.time())
	curr = time.time()
	threshold = 200
	w, h = img.size
	

	for item in range(int(w/2),0,-1):
		if(pix[item,int(h*.3)][0]>threshold):
			print(item)
			if(item>87):
				print("Camera l ", abs(item-203))
			else:
				print("Camera r ", abs(item-203))
			break
		# print(pix[item,int(h*.8)])
		pix[item,int(h*.30)] = (255,255)
	
