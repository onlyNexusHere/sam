import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import time
import cv2


def detect(img):
    img = img[int(img.shape[0]/2):int(img.shape[0]), :, :]
    h, w, _ = img.shape
    img = cv2.GaussianBlur(img, (5, 5), 0)
    hsv_img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    # latest
    yellow_low = np.array([20, 100, 0])
    yellow_high = np.array([255, 255, 255])

    # latest
    white_low = np.array([0, 0, 220])
    white_high = np.array([255, 70, 255])

    # latest
    red_low = np.array([170, 90, 0])
    red_high = np.array([180, 255, 255])

    mask_white = cv2.inRange(hsv_img, white_low, white_high)
    mask_yellow = cv2.inRange(hsv_img, yellow_low, yellow_high)
    mask_red = cv2.inRange(hsv_img, red_low, red_high)

    y_ratio = float(format((mask_yellow > 0).sum() / float(w*h), '.4f'))
    w_ratio = float(format((mask_white > 0).sum() / float(w*h), '.4f'))
    r_ratio = float(format((mask_red > 0).sum() / float(w*h), '.4f'))

    y_thresh = float(0.01)
    w_thresh = float(0.04)
    r_thresh = float(0.18)

    if r_ratio > r_thresh:
        command = 'stop'
        mid = [0, 0]

    elif y_ratio < y_thresh:
        # print('turn left, yellow lane = 0, white lane = 1')
        white_pix_r, white_pix_c = np.where(mask_white > 0)
        min_white_pix_c = min(white_pix_c)
        max_white_pix_c = max(white_pix_c)
        mid = [h - 5, int(((max_white_pix_c - min_white_pix_c) / 2 + min_white_pix_c) / 2)]
        command = 'turn left'

    elif y_ratio >= y_thresh and w_ratio < w_thresh:
        # print('turn right, white lane = 0, yellow lane = 1')
        yellow_pix_r, yellow_pix_c = np.where(mask_yellow > 0)
        min_yellow_pix_c = min(yellow_pix_c)
        max_yellow_pix_c = max(yellow_pix_c)
        max_yellow_pix_r = max(yellow_pix_r)
        lmc = ((max_yellow_pix_c - min_yellow_pix_c) / 2 + min_yellow_pix_c)
        mid = [max_yellow_pix_r, int((w - lmc) / 2 + lmc)]
        command = 'turn right'

    elif y_ratio >= y_thresh and y_ratio >= y_thresh:
        # print('straight, white lane = 1, yellow lane = 1')
        yellow_pix_r, yellow_pix_c = np.where(mask_yellow > 0)
        min_yellow_pix_c = min(yellow_pix_c)
        max_yellow_pix_r = max(yellow_pix_r)
        closer_redge_idx = -1
        bot_arr_rev = img[max_yellow_pix_r][::-1]
        for idx in range(len(bot_arr_rev)):
            if np.average(bot_arr_rev[idx]) <= 200:
                closer_redge_idx = w-1-idx
                break
        mid = [max_yellow_pix_r, int((closer_redge_idx - min_yellow_pix_c)/2 + min_yellow_pix_c)]
        command = 'straight'

    else:
        mid = [-1, -1]

    return int(w/2), mid, command


# for i in range(9, 18):
# for i in range(9):
#     img = np.array(Image.open('1028/test_img/path_' + str(i) + '.jpg'))
#     s = time.time()
#     center, mid, command = detect(img)
#     print(' ')
#     print(center, mid, command)
#     print(time.time() - s)
