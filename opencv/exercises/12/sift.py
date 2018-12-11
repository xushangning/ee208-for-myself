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

    keypoints = []
    for dog in dogs:
        octave_keypoints = []       # all the keypoints in an octave
        for k in range(2):
            img_keypoints = []      # keypoints for an image
            dog_img = dog[k + 1]
            # for each pixel not on the border
            for i in range(1, dog_img.shape[0] - 1):
                for j in range(1, dog_img.shape[1] - 1):
                    # skip pixel with DOG value zero
                    if dog_img[i][j] == 0:
                        continue
                    for offset_i, offset_j in OFFSETS:
                        i_ = i + offset_i
                        j_ = j + offset_j
                        # Note that the offset (0, 0) is also in OFFSETS,
                        # so the condition in if can never be "<=".
                        if (dog_img[i][j] < dog[k][i_][j_]
                                or dog_img[i][j] < dog[k + 2][i_][j_]
                                or dog_img[i][j] < dog_img[i_][j_]):
                            break
                    else:
                        img_keypoints.append((i, j))
            octave_keypoints.append(np.array(img_keypoints, np.int16))

        keypoints.append(octave_keypoints)


if __name__ == '__main__':
    OFFSETS = np.array(((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1),
                        (1, 0), (1, 1), (0, 0)), np.int8)

    img = cv.imread('target.jpg', cv.IMREAD_GRAYSCALE)
    sift(img)
