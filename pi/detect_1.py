import numpy as np
# from scipy.ndimage import gaussian_filter


def detect_mid(img):

    img = img[int(img.shape[0]/2):img.shape[0], :]

    h, w = img.shape

    # img = gaussian_filter(img, sigma=0.5)

    R, C = np.where(img >= 180)

    filtered_R = []
    filtered_C = []

    for i in range(len(R)):
        f_r, f_c = np.where(img[R[i]-50:R[i]+50, C[i]-50:C[i]+50] >= 180)
        if len(f_r) >= 100:
            filtered_R.append(R[i])
            filtered_C.append(C[i])

    for i in range(len(filtered_R)):
        img[filtered_R[i]][filtered_C[i]] = 0

    bottom = max(filtered_R)
    left = min(filtered_C)
    right = max(filtered_C)

    max_rb_idx = np.where(np.array(filtered_C) == right)

    max_rb = max(np.array(filtered_R)[max_rb_idx])

    if max_rb <= (h * 1/2):
        print('One Side Detected')
        right = w
        mid = int(left + ((right - left) / 2))
    else:
        print('Two Sides Detected')
        mid = int(left + ((right - left) / 2))

    # img[bottom-30:bottom-20, left:right] = 0
    # img[bottom-30:bottom-20, mid-10:mid+10] = 255

    return mid
