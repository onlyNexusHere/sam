import numpy as np
from scipy.ndimage import gaussian_filter
import time


def detect_mid(img):

    start = time.time()

    img = img[int(img.shape[0]/2):img.shape[0], :]

    img = gaussian_filter(img, sigma=0.5)

    R, C = np.where(img >= 200)

    bottom = max(R)
    left = min(C)
    right = max(C)

    mid = int(left + ((right - left) / 2))

    img[bottom-30:bottom-20, left:right] = 0
    img[bottom-30:bottom-20, mid-20:mid+20] = 255

    end = time.time()

    print('processing time: ' + str(end - start))

    return mid
