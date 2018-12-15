import numpy as np
import cv2
# from PIL import Image
# import matplotlib.pyplot as plt


def detect(img):

    h, w, _ = img.shape
    img = cv2.GaussianBlur(img, (5, 5), 0)
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # latest
    yellow_low = np.array([20, 43, 46])
    yellow_high = np.array([34, 255, 255])

    # latest
    white_low = np.array([0, 0, 221])
    white_high = np.array([180, 30, 255])

    # latest
    red_low = np.array([0, 43, 46])
    red_high = np.array([10, 255, 255])

    # latest
    green_low = np.array([30, 0, 255])
    green_high = np.array([80, 200, 255])

    r_thresh = float(0.04)
    y_thresh = float(0.005)
    w_thresh = float(0.005)
    g_thresh = float(0.0045)

    center = int(w / 2)

    # detect red
    mask_red = cv2.inRange(hsv_img, red_low, red_high)
    mask_red = mask_red / 255.0
    r_ratio = float(format(np.sum(mask_red) / float(w * h), '.4f'))

    # if red detected
    if r_ratio >= r_thresh:

        mask_green = cv2.inRange(hsv_img, green_low, green_high)
        mask_green = mask_green / 255.0
        g_ratio = float(format(np.sum(mask_green) / float(w * h), '.4f'))

        ratio = 'red: ' + str(r_ratio) + ' ' + 'green: ' + str(g_ratio)

        # if green detected
        if g_ratio >= g_thresh:
            command = 'green'
            return center, -1, command, ratio

        # if green not detected
        else:
            command = 'stop'
            return center, -1, command, ratio

    # if red not detected
    else:

        mask_yellow = cv2.inRange(hsv_img, yellow_low, yellow_high)
        mask_white = cv2.inRange(hsv_img, white_low, white_high)
        mask_yellow = mask_yellow / 255.0
        mask_white = mask_white / 255.0

        y_ratio = float(format(np.sum(mask_yellow) / float(w * h), '.4f'))
        w_ratio = float(format(np.sum(mask_white) / float(w * h), '.4f'))

        ratio = 'yellow: ' + str(y_ratio) + ' ' + 'white: ' + str(w_ratio)

        # print("AVG WHITE ", np.median(np.where(mask_white >0)))
        # print("AVG YELLOW ", np.median(np.where(mask_yellow >0)))

        # no yellow detected, white detected, turn left
        if y_ratio < y_thresh and w_ratio >= w_thresh:

            _, white_pix_c = np.where(mask_white > 0)

            if len(white_pix_c) == 0:
                print('111111')
                command = 'unknown'
                return center, 510, command, ratio
            else:
                command = 'left'
                mwc = np.median(white_pix_c)
                return center, int(mwc - 250), command, ratio

        # no white detected, yellow detected, turn right
        elif y_ratio >= y_thresh and w_ratio < w_thresh:

            _, yellow_pix_c = np.where(mask_yellow > 0)

            if len(yellow_pix_c) == 0:
                command = 'unknown'
                print('22222222')
                return center, 510, command, ratio
            else:
                command = 'right'
                myc = np.median(yellow_pix_c)
                #return center, int(myc + ((w - myc) / 2)), command, ratio
                return center, int(myc + 230), command, ratio

        # yellow detected, white detected, go straight
        elif y_ratio >= y_thresh and w_ratio >= w_thresh:

            mask_yellow = mask_yellow[:, 0:int(mask_yellow.shape[1]/2)]
            mask_white = mask_white[:, int(mask_white.shape[1]/2): mask_white.shape[1]]

            _, yellow_pix_c = np.where(mask_yellow > 0)
            _, white_pix_c = np.where(mask_white > 0)

            # if len(white_pix_c) == 0 or len(yellow_pix_c) == 0:
            #     print('333333333333')
            #     command = 'unknown'
            #     return center, 510, command, ratio
            #
            # else:
            #     command = 'straight'
            #     myc = np.median(yellow_pix_c)
            #     mwc = np.median(white_pix_c) + center
            #     return center, int(myc + ((mwc - myc) / 2)), command, ratio

            if len(white_pix_c) != 0 or len(yellow_pix_c) != 0:
                command = 'straight'
                myc = np.median(yellow_pix_c)
                mwc = np.median(white_pix_c) + center
                return center, int(myc + ((mwc - myc) / 2)), command, ratio


        # no white detected, no yellow detected
        else:
            print('4444444')
            command = 'unknown'
            return center, center, command, ratio


# fname = 'small/'
#
# for i in range(5):
#     img = np.array(Image.open(fname + str(i) + '.jpg'))
#
#     # img, center, mid, command, ratio = detect(img)
#
#     img = detect(img)
#
#     plt.subplot(3, 3, i + 1)
#     plt.imshow(img)
#     # plt.title(ratio)
#
# plt.subplots_adjust(hspace=0.5, wspace=0.5)
# plt.show()







    # r_ratio = float(format((mask_red > 0).sum() / float(w * h), '.4f'))

    # if r_ratio >= r_thresh:
    #
    #     mask_green = cv2.inRange(hsv_img, green_low, green_high)
    #     g_ratio = float(format((mask_green > 0).sum() / float(w * h), '.4f'))
    #
    #     ratio = [r_ratio, g_ratio]
    #
    #     if g_ratio >= g_thresh:
    #         command = 'green light'
    #         return center, 0, command, ratio
    #     else:
    #         command = 'stop'
    #         return center, 0, command, ratio
    #
    # else:
    #     mask_yellow = cv2.inRange(hsv_img, yellow_low, yellow_high)
    #     mask_white = cv2.inRange(hsv_img, white_low, white_high)
    #     y_ratio = float(format((mask_yellow > 0).sum() / float(w * h), '.4f'))
    #     w_ratio = float(format((mask_white > 0).sum() / float(w * h), '.4f'))
    #
    #     ratio = [y_ratio, w_ratio]
    #
    #     if y_ratio < y_thresh:
    #
    #         _, white_pix_c = np.where(mask_white > 0)
    #
    #         if len(white_pix_c) == 0:
    #             command = 'stop'
    #             return center, center, command, ratio
    #         else:
    #             command = 'turn left'
    #             return center, int(np.median(white_pix_c) / 2), command, ratio
    #
    #     elif y_ratio >= y_thresh and w_ratio < w_thresh:
    #
    #         _, yellow_pix_c = np.where(mask_yellow > 0)
    #
    #         if len(yellow_pix_c) == 0:
    #             command = 'stop'
    #             return center, center, command, ratio
    #         else:
    #             command = 'turn right'
    #             myc = np.median(yellow_pix_c)
    #             return center, int(myc + ((w - myc) / 2)), command, ratio
    #
    #     elif y_ratio >= y_thresh and w_ratio >= w_thresh:
    #
    #         _, white_pix_c = np.where(mask_white > 0)
    #         _, yellow_pix_c = np.where(mask_yellow > 0)
    #
    #         if len(white_pix_c) == 0 or len(yellow_pix_c) == 0:
    #             command = 'stop'
    #             return center, center, command, ratio
    #
    #         # elif int(max(white_pix_c) - min(white_pix_c)) < int(150):
    #         elif int(min(white_pix_c)) > int(h/2):
    #             command = 'turn right'
    #             myc = np.median(yellow_pix_c)
    #             return center, int(myc + ((w - myc) / 2)), command, ratio
    #         else:
    #             command = 'straight'
    #             mwc = np.median(white_pix_c)
    #             myc = np.median(yellow_pix_c)
    #             return center, int(myc + ((mwc - myc) / 2)), command, ratio
    #
    #     else:
    #         command = 'unknown state'
    #         return center, -1, command, []
