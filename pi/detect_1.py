import numpy as np
# from scipy.ndimage import gaussian_filter


def detect_mid(img):
    threshold = 200
    w, h = img.size
    
    middle=86
    for item in range(int(w/2),0,-1):

        if(pix[item,int(h*.35)][0]>threshold):
            #print(item)
            if(item>middle):
            print("Camera l ", abs(item-203))

        #if(pix[item,int(h*.30)][0]>threshold):
            #if(item>middle):
                #print("Camera l ", abs(item-middle))
                #break

            #else:
                #break
                #print("Camera r ", abs(item-middle))
            break
        # print(pix[item,int(h*.8)])
        #pix[item,int(h*.35)] = (255,255)

    adjustment = item-middle
    print(adjustment)
