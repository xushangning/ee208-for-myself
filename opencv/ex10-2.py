from math import sqrt, floor

import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv

for count in range(2):
    filename = 'img{}.png'.format(count + 1)
    img = cv.imread('../instructions/10/images/' + filename, cv.IMREAD_GRAYSCALE)

    plt.subplot(2, 1, count + 1)
    plt.title('Grayscale Histogram of ' + filename)
    # plot a normalised histogram
    plt.hist(img.ravel(), 256, (0, 256), density=True, stacked=True)
plt.tight_layout()
plt.savefig('grayscale_hist.png')
plt.close()     # done with the first plot

for count in range(2):
    filename = 'img{}.png'.format(count + 1)
    img = cv.imread('../instructions/10/images/' + filename, cv.IMREAD_GRAYSCALE)

    # find the gradient
    gradient = np.zeros((img.shape[0] - 2, img.shape[1] - 2), dtype=np.int16)
    for i in range(1, img.shape[0] - 1):
        for j in range(1, img.shape[1] - 1):
            # Integers must be promoted otherwise they will overflow.
            dx = int(img[i][j + 1]) - img[i][j - 1]     # derivative in rows
            dy = int(img[i + 1][j]) - img[i - 1][j]     # derivative in columns
            gradient[i - 1][j - 1] = floor(sqrt(dx * dx + dy * dy))

    plt.subplot(2, 1, count + 1)
    plt.title('HOG of ' + filename)
    plt.hist(gradient.ravel(), 360, (0, 360), density=True, stacked=True)
plt.tight_layout()
plt.savefig('hog.png')
