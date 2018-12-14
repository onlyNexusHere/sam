import numpy as np
import cv2


def detect(img):
    img = img[int(img.shape[0]/2):int(img.shape[0]), :, :]
    h, w, _ = img.shape
    img = cv2.GaussianBlur(img, (5, 5), 0)
    hsv_img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    # latest
    yellow_low = np.array([26, 30, 46])
    yellow_high = np.array([34, 255, 255])

    # latest
    white_low = np.array([0, 0, 200])
    white_high = np.array([180, 30, 255])

    # latest
    red_low = np.array([0, 90, 0])
    red_high = np.array([10, 255, 255])

    mask_white = cv2.inRange(hsv_img, white_low, white_high)
    mask_yellow = cv2.inRange(hsv_img, yellow_low, yellow_high)
    mask_red = cv2.inRange(hsv_img, red_low, red_high)

    y_ratio = float(format((mask_yellow > 0).sum() / float(w*h), '.4f'))
    w_ratio = float(format((mask_white > 0).sum() / float(w*h), '.4f'))
    r_ratio = float(format((mask_red > 0).sum() / float(w*h), '.4f'))

    y_thresh = float(0.01)
    w_thresh = float(0.02)
    r_thresh = float(0.25)

    print(y_ratio, w_ratio, y_ratio)

    if r_ratio >= r_thresh:
        command = 'stop'
        mid = 0

    elif y_ratio < y_thresh:
        _, white_pix_c = np.where(mask_white > 0)
        if len(white_pix_c) == 0:
            mid = int(w/2)
            command = 'straight'
        else:
            mid = int(np.median(white_pix_c)/2)
            command = 'turn left'

    elif y_ratio >= y_thresh and w_ratio < w_thresh:
        _, yellow_pix_c = np.where(mask_yellow > 0)
        if len(yellow_pix_c) == 0:
            mid = int(w/2)
            command = 'straight'
        else:
            myc = np.median(yellow_pix_c)
            mid = int(myc+((w-myc)/2))
            command = 'turn right'

    elif y_ratio >= y_thresh and w_ratio >= w_thresh:
        _, white_pix_c = np.where(mask_white > 0)
        _, yellow_pix_c = np.where(mask_yellow > 0)
        if len(white_pix_c) == 0 or len(yellow_pix_c) == 0:
            mid = int(w / 2)
            command = 'straight'
        else:
            mwc = np.median(white_pix_c)
            myc = np.median(yellow_pix_c)
            mid = int(myc + ((mwc - myc) / 2))
            command = 'straight'

    else:
        mid = -1

    return int(w/2), mid, command, [y_ratio, w_ratio, r_ratio]


# for i in range(9):
#     img = np.array(Image.open('1028/test_img/path_' + str(i) + '.jpg'))
#     s = time.time()
#     center, mid, command = detect(img)
#     print(' ')
#     print(center, mid, command)
#     print(time.time() - s)
