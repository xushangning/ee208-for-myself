import numpy as np
import cv2 as cv

# offsets used in calculating descriptors
OFFSETS = np.array([
 [[-7.5, -7.5], [-7.5, -6.5], [-7.5, -5.5], [-7.5, -4.5],
  [-7.5, -3.5], [-7.5, -2.5], [-7.5, -1.5], [-7.5, -0.5],
  [-7.5, 0.5], [-7.5, 1.5], [-7.5, 2.5], [-7.5, 3.5],
  [-7.5, 4.5], [-7.5, 5.5], [-7.5, 6.5], [-7.5, 7.5]],
 [[-6.5, -7.5], [-6.5, -6.5], [-6.5, -5.5], [-6.5, -4.5],
  [-6.5, -3.5], [-6.5, -2.5], [-6.5, -1.5], [-6.5, -0.5],
  [-6.5, 0.5], [-6.5, 1.5], [-6.5, 2.5], [-6.5, 3.5],
  [-6.5, 4.5], [-6.5, 5.5], [-6.5, 6.5], [-6.5, 7.5]],
 [[-5.5, -7.5], [-5.5, -6.5], [-5.5, -5.5], [-5.5, -4.5],
  [-5.5, -3.5], [-5.5, -2.5], [-5.5, -1.5], [-5.5, -0.5],
  [-5.5, 0.5], [-5.5, 1.5], [-5.5, 2.5], [-5.5, 3.5],
  [-5.5, 4.5], [-5.5, 5.5], [-5.5, 6.5], [-5.5, 7.5]],
 [[-4.5, -7.5], [-4.5, -6.5], [-4.5, -5.5], [-4.5, -4.5],
  [-4.5, -3.5], [-4.5, -2.5], [-4.5, -1.5], [-4.5, -0.5],
  [-4.5, 0.5], [-4.5, 1.5], [-4.5, 2.5], [-4.5, 3.5],
  [-4.5, 4.5], [-4.5, 5.5], [-4.5, 6.5], [-4.5, 7.5]],
 [[-3.5, -7.5], [-3.5, -6.5], [-3.5, -5.5], [-3.5, -4.5],
  [-3.5, -3.5], [-3.5, -2.5], [-3.5, -1.5], [-3.5, -0.5],
  [-3.5, 0.5], [-3.5, 1.5], [-3.5, 2.5], [-3.5, 3.5],
  [-3.5, 4.5], [-3.5, 5.5], [-3.5, 6.5], [-3.5, 7.5]],
 [[-2.5, -7.5], [-2.5, -6.5], [-2.5, -5.5], [-2.5, -4.5],
  [-2.5, -3.5], [-2.5, -2.5], [-2.5, -1.5], [-2.5, -0.5],
  [-2.5, 0.5], [-2.5, 1.5], [-2.5, 2.5], [-2.5, 3.5],
  [-2.5, 4.5], [-2.5, 5.5], [-2.5, 6.5], [-2.5, 7.5]],
 [[-1.5, -7.5], [-1.5, -6.5], [-1.5, -5.5], [-1.5, -4.5],
  [-1.5, -3.5], [-1.5, -2.5], [-1.5, -1.5], [-1.5, -0.5],
  [-1.5, 0.5], [-1.5, 1.5], [-1.5, 2.5], [-1.5, 3.5],
  [-1.5, 4.5], [-1.5, 5.5], [-1.5, 6.5], [-1.5, 7.5]],
 [[-0.5, -7.5], [-0.5, -6.5], [-0.5, -5.5], [-0.5, -4.5],
  [-0.5, -3.5], [-0.5, -2.5], [-0.5, -1.5], [-0.5, -0.5],
  [-0.5, 0.5], [-0.5, 1.5], [-0.5, 2.5], [-0.5, 3.5],
  [-0.5, 4.5], [-0.5, 5.5], [-0.5, 6.5], [-0.5, 7.5]],
 [[0.5, -7.5], [0.5, -6.5], [0.5, -5.5], [0.5, -4.5],
  [0.5, -3.5], [0.5, -2.5], [0.5, -1.5], [0.5, -0.5],
  [0.5, 0.5], [0.5, 1.5], [0.5, 2.5], [0.5, 3.5],
  [0.5, 4.5], [0.5, 5.5], [0.5, 6.5], [0.5, 7.5]],
 [[1.5, -7.5], [1.5, -6.5], [1.5, -5.5], [1.5, -4.5],
  [1.5, -3.5], [1.5, -2.5], [1.5, -1.5], [1.5, -0.5],
  [1.5, 0.5], [1.5, 1.5], [1.5, 2.5], [1.5, 3.5],
  [1.5, 4.5], [1.5, 5.5], [1.5, 6.5], [1.5, 7.5]],
 [[2.5, -7.5], [2.5, -6.5], [2.5, -5.5], [2.5, -4.5],
  [2.5, -3.5], [2.5, -2.5], [2.5, -1.5], [2.5, -0.5],
  [2.5, 0.5], [2.5, 1.5], [2.5, 2.5], [2.5, 3.5],
  [2.5, 4.5], [2.5, 5.5], [2.5, 6.5], [2.5, 7.5]],
 [[3.5, -7.5], [3.5, -6.5], [3.5, -5.5], [3.5, -4.5],
  [3.5, -3.5], [3.5, -2.5], [3.5, -1.5], [3.5, -0.5],
  [3.5, 0.5], [3.5, 1.5], [3.5, 2.5], [3.5, 3.5],
  [3.5, 4.5], [3.5, 5.5], [3.5, 6.5], [3.5, 7.5]],
 [[4.5, -7.5], [4.5, -6.5], [4.5, -5.5], [4.5, -4.5],
  [4.5, -3.5], [4.5, -2.5], [4.5, -1.5], [4.5, -0.5],
  [4.5, 0.5], [4.5, 1.5], [4.5, 2.5], [4.5, 3.5],
  [4.5, 4.5], [4.5, 5.5], [4.5, 6.5], [4.5, 7.5]],
 [[5.5, -7.5], [5.5, -6.5], [5.5, -5.5], [5.5, -4.5],
  [5.5, -3.5], [5.5, -2.5], [5.5, -1.5], [5.5, -0.5],
  [5.5, 0.5], [5.5, 1.5], [5.5, 2.5], [5.5, 3.5],
  [5.5, 4.5], [5.5, 5.5], [5.5, 6.5], [5.5, 7.5]],
 [[6.5, -7.5], [6.5, -6.5], [6.5, -5.5], [6.5, -4.5],
  [6.5, -3.5], [6.5, -2.5], [6.5, -1.5], [6.5, -0.5],
  [6.5, 0.5], [6.5, 1.5], [6.5, 2.5], [6.5, 3.5],
  [6.5, 4.5], [6.5, 5.5], [6.5, 6.5], [6.5, 7.5]],
 [[7.5, -7.5], [7.5, -6.5], [7.5, -5.5], [7.5, -4.5],
  [7.5, -3.5], [7.5, -2.5], [7.5, -1.5], [7.5, -0.5],
  [7.5, 0.5], [7.5, 1.5], [7.5, 2.5], [7.5, 3.5],
  [7.5, 4.5], [7.5, 5.5], [7.5, 6.5], [7.5, 7.5]]])


def sift(img):
    keypoints = cv.goodFeaturesToTrack(img, 0, 0.01, 10).reshape(-1, 2)

    dy = img[2:, 1:-1] - img[:-2, 1:-1]
    dx = img[1:-1, 2:] - img[1:-1, :-2]
    # if the image is m * n, the mags and angles array are (m - 2) * (n - 2)
    mags = np.sqrt(dx * dx + dy * dy)
    angles = np.arctan2(dy, dx) / np.pi * 180 + 180
    # find orientation for each keypoint
    keypoints_with_orientation = []
    for x, y in keypoints:
        x = int(x)
        y = int(y)
        # if the neighborhood sits next to the border
        if x < 3 or x + 3 > img.shape[0] or y < 3 or y + 3 > img.shape[1]:
            continue

        mag_part = mags[y - 3: y + 1, x - 3: x + 1]
        angle_part = angles[y - 3: y + 1, x - 3: x + 1]
        histogram = np.histogram(angle_part, 36, (0, 360), weights=mag_part)[0]
        threshold = histogram.max() * 0.8
        for i, weight in enumerate(histogram):
            if weight > threshold:
                keypoints_with_orientation.append((x, y, i * 10 + 5))

    # generate descriptors
    descriptors = []
    for x, y, orientation in keypoints_with_orientation:
        max_offset = 7.5 * np.sqrt(2) * np.sin((orientation / 90 + 45) / 180 * np.pi)
        # reject the keypoint if a descriptor can not be generated due to border
        if y + np.ceil(max_offset) > img.shape[0] or np.floor(y - max_offset) < 0 \
                or x + np.ceil(max_offset) > img.shape[1] or np.floor(x - max_offset) < 0:
            continue

        rotation_matrix = np.array([
            [np.cos(orientation), - np.sin(orientation)],
            [np.sin(orientation), np.cos(orientation)]
        ])
        # find the rotated offsets
        rotated_offsets = np.array([[rotation_matrix @ j for j in i] for i in OFFSETS])

        descriptor = []
        # for each 4 * 4 window
        for i in range(4):
            for j in range(4):
                window = rotated_offsets[4 * i: 4 * (i + 1), 4 * j: 4 * (j + 1), :]
                angle_results = np.zeros((4, 4))
                for k in range(4):
                    for l in range(4):
                        x_ = x + window[k][l][0]
                        y_ = y + window[k][l][1]
                        floored_x_ = np.floor(x_)
                        floored_y_ = np.floor(y_)

                        dx1 = x_ - floored_x_
                        dx2 = 1 - dx1
                        dy1 = y_ - floored_y_
                        dy2 = 1 - dy1

                        angle_results[k][l] = angles[y][x] * dx2 * dy2 \
                            + angles[y][x + 1] * dx1 * dy2 \
                            + angles[y + 1][x] * dx2 * dy1 \
                            + angles[y + 1][x + 1] * dx1 * dy1 \
                            - orientation
                hist = np.histogram(angle_results, 8, (0, 360))[0]
                descriptor.append(hist)
        descriptor = np.array(descriptor).reshape(128)
        norm = np.sqrt((descriptor ** 2).sum())
        if int(norm):
            descriptor = descriptor / norm
            descriptors.append(descriptor)
    return np.array(descriptors).reshape(-1, 128)


if __name__ == '__main__':
    img = cv.imread('target.jpg', cv.IMREAD_GRAYSCALE)
    descriptors1 = sift(img)
    imgs = [cv.imread('dataset/{}.jpg'.format(i), cv.IMREAD_GRAYSCALE) for i in range(1, 6)]
    for i in range(5):
        descriptors = sift(imgs[i])
        distance = 0
        for d1 in descriptors1:
            for d in descriptors:
                distance += d1 @ d
        print(i + 1, distance)
