import os

import numpy as np
import cv2 as cv

img = cv.imread('1.jpg', cv.IMREAD_GRAYSCALE)

dx = cv.Sobel(img, cv.CV_32F, 1, 0)
dy = cv.Sobel(img, cv.CV_32F, 0, 1)
mag = np.sqrt(dx * dx + dy * dy)
tangents = dy / (dx + 1e-6)

# Non-maximum suppression
suppressed_mag = np.copy(mag)
for i in range(1, mag.shape[0] - 1):
    for j in range(1, mag.shape[1] - 1):
        if tangents[i][j] >= 1:
            cot = 1 / tangents[i][j]
            # Interpolate the upper gradient. "Upper" means the direction
            # in which y is increasing.
            mag_upper = mag[i + 1][j] * (1 - cot) + mag[i + 1][j + 1] * cot
            # interpolate the lower gradient
            mag_lower = mag[i - 1][j] * (1 - cot) + mag[i - 1][j - 1] * cot
        elif tangents[i][j] >= 0:
            mag_upper = mag[i][j + 1] * (1 - tangents[i][j]) + mag[i + 1][j + 1] * tangents[i][j]
            mag_lower = mag[i][j - 1] * (1 - tangents[i][j]) + mag[i - 1][j - 1] * tangents[i][j]
        elif tangents[i][j] >= -1:
            mag_upper = mag[i][j - 1] * (1 + tangents[i][j]) - mag[i + 1][j - 1] * tangents[i][j]
            mag_lower = mag[i][j + 1] * (1 + tangents[i][j]) - mag[i - 1][j + 1] * tangents[i][j]
        else:
            cot = 1 / tangents[i][j]
            mag_upper = mag[i + 1][j] * (1 + cot) - mag[i + 1][j - 1] * cot
            mag_lower = mag[i - 1][j] * (1 + cot) - mag[i - 1][j + 1] * cot

        # intensity at (i, j) is not greater than its neighbors
        if mag[i][j] <= mag_lower or mag[i][j] <= mag_upper:
            suppressed_mag[i][j] = 0

mag = suppressed_mag

for low in range(20, 160, 10):
    for high in range(low + 10, min(4 * low, 300) + 10, 10):
        print(low, high)
        OUTPUT_FOLDER_NAME = 'canny_output/{}_{}'.format(low, high)
        if not os.path.exists(OUTPUT_FOLDER_NAME):
            os.mkdir(OUTPUT_FOLDER_NAME)

        edges = np.zeros(img.shape, np.uint8)
        # double thresholds
        edges[mag >= high] = 255
        cv.imwrite(OUTPUT_FOLDER_NAME + '/1_2t.png', edges)

        OFFSETS = np.array(((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1),
                            (1, 0), (1, 1)), np.int8)
        # hysteresis
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                if mag[i][j] >= low:
                    for offset_i, offset_j in OFFSETS:
                        i_ = i + offset_i
                        j_ = j + offset_j
                        if 0 <= i_ < img.shape[0] and 0 <= j_ < img.shape[1]:
                            if mag[i_][j_] >= high:
                                edges[i][j] = 255
                                break
        cv.imwrite(OUTPUT_FOLDER_NAME + '/1_final.png', edges)
        cv.imwrite(OUTPUT_FOLDER_NAME + '/1_built_in.png', cv.Canny(img, low, high))
