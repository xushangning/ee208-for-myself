import timeit

import cv2 as cv

from canny import canny

for i in range(1, 4):
    print(i)
    img = cv.imread('{}.jpg'.format(i), cv.IMREAD_GRAYSCALE)
    print(timeit.timeit('canny(img, 20, 80)', number=100, globals=globals()))
    print(timeit.timeit('cv.Canny(img, 20, 80)', number=100, globals=globals()))
