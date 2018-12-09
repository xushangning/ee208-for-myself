import numpy as np
import cv2 as cv


def sift(img):
    # create 4 octaves
    scale = np.sqrt(2)
    # add the doubled and the original image to the seed
    octave_seed = [cv.resize(img, (0, 0), fx=scale, fy=scale), img]
    scale = np.sqrt(2) / 2
    for _ in range(2):
        octave_seed.append(cv.resize(img, (0, 0), fx=scale, fy=scale, interpolation=cv.INTER_AREA))
        scale /= np.sqrt(2)

    # successively blur the image in each octave
    octaves = []
    for i, seed in enumerate(octave_seed):
        scale = np.sqrt(2) / 2 * (i + 1)
        octave = [seed] + [cv.GaussianBlur(seed, (3, 3), scale * np.sqrt(2) ** j)
                           for j in range(1, 5)]
        octaves.append(np.array(octave, np.uint8))

    # Difference of Gaussian
    dogs = [np.array([octave[i].astype(np.int16) - octave[i + 1]
                      for i in range(4)], np.int16) for octave in octaves]


if __name__ == '__main__':
    img = cv.imread('target.jpg', cv.IMREAD_GRAYSCALE)
    sift(img)
