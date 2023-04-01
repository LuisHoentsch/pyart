import cv2
import numpy as np


def quantize_cv2(img, k):
    x = img.reshape((-1, 1))
    x = np.float32(x)  # convert to np.float32

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

    ret, label, center = cv2.kmeans(x, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # Now convert back into uint8, and make original image
    center = np.uint8(center)
    res = center[label.flatten()]
    res2 = res.reshape(img.shape)
    return res2


def openclose(img, kernel):
    return cv2.morphologyEx(cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel), cv2.MORPH_CLOSE, kernel)


def color(img, colora, colorb):
    colorgradient = {color: [int(a * (color / 255) + b * (1 - color / 255)) for a, b in zip(colora, colorb)] for color
                     in np.unique(img)}
    res = [[colorgradient[img[i][j]] for j in range(len(img[i]))] for i in range(len(img))]
    return np.array(res)[:, :, [2, 1, 0]]


def hex_to_rgb(hex_string):
    hex_string = hex_string.lstrip('#')
    return tuple(int(hex_string[i:i+2], 16) for i in (0, 2, 4))


def alter_image(file, colora, colorb):
    img = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_GRAYSCALE)
    q = quantize_cv2(img, 10)
    openclose1 = openclose(q, np.ones((2, 2), np.uint8))
    openclose2 = openclose(openclose1, np.ones((3, 3), np.uint8))
    openclose3 = openclose(openclose2, np.ones((4, 4), np.uint8))
    colored = color(openclose3, hex_to_rgb(colora), hex_to_rgb(colorb))

    return colored


'''
Possible TODOs

- Recognize background and make it white / transparent
- Select colors for coloring from image
- Show input and output image on webserver and have download button
'''