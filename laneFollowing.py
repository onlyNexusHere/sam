import numpy as np
from PIL import Image, ImageDraw

#...

img = Image.open('RoadTestIm.jpg').convert('LA')
pix = img.load()

threshold = 200

# data[5]=(255,255)


# for i in range(0,500):
# 	for j in range(0,500):
# 		pix[i,j]=(100,255)

#Cropping for debugging

w, h = img.size
#img = img.crop((w*.1, h*.8, w-w*.2, h))
#w, h = img.size
# pix = img.load()
# draw = ImageDraw.Draw(img)


#Boundary markers for debugging
#draw.ellipse((20, 20, 80, 40), fill = 'blue', outline ='blue')


rightPoint = pix[int(w*.95),int(h*.2)]
leftPoint = pix[int(w*.85),int(h*.2)]

#For right side up image
# for item in range(w-1,0,-1):
# 	if(pix[item,int(h*.8)][0]>threshold):
# 		print(item)
# 		break
# 	# print(pix[item,int(h*.8)])
# 	pix[item,int(h*.8)] = (255,255)
	

for item in range(0,w-1):
	if(pix[item,int(h*.35)][0]>threshold):
		print(item)
		break
	# print(pix[item,int(h*.8)])
	pix[item,int(h*.35)] = (255,255)
	

#Turns points white for debugging

# pix[int(w*.83),int(h*.8)] = (255,255)
# pix[int(w*.55),int(h*.8)] = (255,255)

# for i in pix[int(w*.83),:]:
# 	print(i)



rows,columns = img.size
img.show()
