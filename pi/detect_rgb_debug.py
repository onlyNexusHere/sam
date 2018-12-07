import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import time
import cv2


def detect(img):
    img = img[int(img.shape[0]/2):int(img.shape[0]), :, :]
    # img = img[int(img.shape[0]/4):int(img.shape[0]*3/4), :, :]
    h, w, _ = img.shape
    # img = gaussian_filter(img, sigma=0.8)
    # img = cv2.medianBlur(img, 5)
    img = cv2.GaussianBlur(img, (5, 5), 0)
    hsv_img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    # v = hsv_img[:, :, 2]
    # max_v = np.max(v)
    # min_v = np.min(v)
    # new_v = (v / 255 - v) / (max_v - min_v)
    # hsv_img[:, :, 2] = new_v

    # v = hsv_img[:, :, 2]
    # max_v = np.max(v)
    # min_v = np.min(v)
    # new_v = (v / 255 - min_v) / (max_v - min_v)
    # hsv_img[:, :, 2] = new_v

    # s = hsv_img[:, :, 0]
    # max_s = np.max(s)
    # min_s = np.min(s)
    # new_s = (s / 255 - s) / (max_s - min_s)
    # hsv_img[:, :, 0] = new_s

    # yellow_low = np.array([20, 100, 100])
    # yellow_high = np.array([30, 255, 255])

    # white_low = np.array([0, 100, 230])
    # white_high = np.array([255, 255, 255])

    # yellow_low = np.array([20, 70, 0])
    # yellow_high = np.array([30, 255, 245])


    # latest
    yellow_low = np.array([20, 50, 0])
    yellow_high = np.array([30, 250, 255])

    # latest
    white_low = np.array([0, 0, 200])
    white_high = np.array([255, 80, 255])

    # latest
    red_low = np.array([170, 90, 0])
    red_high = np.array([180, 255, 255])

    mask_white = cv2.inRange(hsv_img, white_low, white_high)
    mask_yellow = cv2.inRange(hsv_img, yellow_low, yellow_high)
    mask_red = cv2.inRange(hsv_img, red_low, red_high)
    mask = mask_yellow + mask_white + mask_red
    # mask = cv2.bitwise_or(mask_white, mask_yellow)

    y_ratio = float(format((mask_yellow > 0).sum() / float(w*h), '.4f'))
    w_ratio = float(format((mask_white > 0).sum() / float(w*h), '.4f'))
    r_ratio = float(format((mask_red > 0).sum() / float(w*h), '.4f'))
    # r_ratio = 0.01

    y_thresh = float(0.01)
    w_thresh = float(0.04)
    r_thresh = float(0.25)

    if r_ratio > r_thresh:
        # print('ready to stop')
        command = 'stop'
        mid = [0, 0]

    elif y_ratio < y_thresh:
        print('turn left, yellow lane = 0, white lane = 1')
        white_pix_r, white_pix_c = np.where(mask_white > 0)
        min_white_pix_c = min(white_pix_c)
        max_white_pix_c = max(white_pix_c)
        mid = [h - 5, int(((max_white_pix_c - min_white_pix_c) / 2 + min_white_pix_c) / 2)]
        command = 'turn left'

    elif y_ratio >= y_thresh and w_ratio < w_thresh:
        print('turn right, white lane = 0, yellow lane = 1')
        yellow_pix_r, yellow_pix_c = np.where(mask_yellow > 0)
        min_yellow_pix_c = min(yellow_pix_c)
        max_yellow_pix_c = max(yellow_pix_c)
        max_yellow_pix_r = max(yellow_pix_r)
        lmc = ((max_yellow_pix_c - min_yellow_pix_c) / 2 + min_yellow_pix_c)
        mid = [max_yellow_pix_r, min_yellow_pix_c, int((w - lmc) / 2 + lmc)]
        command = 'turn right'

    elif y_ratio >= y_thresh and y_ratio >= y_thresh:
        print('straight, white lane = 1, yellow lane = 1')
        yellow_pix_r, yellow_pix_c = np.where(mask_yellow > 0)
        min_yellow_pix_c = min(yellow_pix_c)
        max_yellow_pix_r = max(yellow_pix_r)
        closer_redge_idx = -1
        bot_arr_rev = img[max_yellow_pix_r][::-1]
        for idx in range(len(bot_arr_rev)):
            if np.average(bot_arr_rev[idx]) <= 200:
                closer_redge_idx = w-1-idx
                break
        mid = [max_yellow_pix_r, min_yellow_pix_c, int((closer_redge_idx - min_yellow_pix_c)/2 + min_yellow_pix_c)]
        command = 'straight'

    else:
        # print('unknown state, yellow lane = 0, white lane = 0')
        # command = 'unknown state'
        mid = [-1, -1]

    center = int(w/2)
    result = cv2.bitwise_and(img, img, mask=mask)
    command += str([y_ratio, w_ratio, r_ratio])
    return result, center, mid, command, [y_ratio, w_ratio, r_ratio]
    # return result, y_ratio


# for i in range(9, 18):
for i in range(9):
    img = np.array(Image.open('1920/test_img/path_' + str(i) + '.jpg'))
    img, center, mid, command, ratios = detect(img)
    # img, w_ratio = detect(img)
    print(center, mid)
    if command == 'straight' + str(ratios):
    # if command == 'straight':
        mid_r, ledge, mid_c = mid
        img[mid_r - 100:mid_r-80, ledge:int(mid_c * 2), :] = [255, 255, 255]
        img[mid_r - 125:mid_r - 60, mid_c - 30:mid_c + 30, :] = [255, 255, 255]
    elif command == 'turn left' + str(ratios):
    # elif command == 'turn left':
        mid_r, mid_c = mid
        img[mid_r - 200:mid_r - 180, 0:int(mid_c * 2), :] = [255, 255, 255]
        img[mid_r - 220:mid_r - 160, mid_c - 30:mid_c + 30, :] = [255, 255, 255]
    elif command == 'turn right' + str(ratios):
    # elif command == 'turn right':
        mid_r, ledge, mid_c = mid
        img[mid_r - 200:mid_r - 180, ledge:int(mid_c * 2), :] = [255, 255, 255]
        img[mid_r - 220:mid_r - 160, mid_c - 30:mid_c + 30, :] = [255, 255, 255]
    elif command == 'stop' + str(ratios):
        print('ready to stop')
    else:
        print('unknown state')

    plt.subplot(3, 3, i+1)
    plt.imshow(img)
    plt.title(command)

plt.subplots_adjust(hspace=0.5, wspace=0.5)
plt.show()
