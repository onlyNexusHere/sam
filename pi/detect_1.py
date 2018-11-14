import numpy as np
# from scipy.ndimage import gaussian_filter


def detect_mid(img):
    threshold = 200
    w, h = img.size
    
    middle=86
    for item in range(int(w/2),0,-1):

        if(pix[item,int(h*.35)][0]>threshold):
            break

    adjustment = item-middle
    return adjustment
