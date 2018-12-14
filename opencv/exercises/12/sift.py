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
    keypoints = []
    for x, y, orientation in keypoints_with_orientation:
        max_offset = 7.5 * np.sqrt(2) * np.sin((orientation / 90 + 45) / 180 * np.pi)
        # reject the keypoint if a descriptor can not be generated due to border
        if y + np.ceil(max_offset) > img.shape[0] or np.floor(y - max_offset) < 0 \
                or x + np.ceil(max_offset) > img.shape[1] or np.floor(x - max_offset) < 0:
            continue

        rad = np.deg2rad(orientation)
        rotation_matrix = np.array([
            [np.cos(rad), - np.sin(rad)], [np.sin(rad), np.cos(rad)]
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

                        angle_results[k][l] = angles[y - 1][x - 1] * dx2 * dy2 \
                            + angles[y - 1][x] * dx1 * dy2 \
                            + angles[y][x - 1] * dx2 * dy1 \
                            + angles[y][x] * dx1 * dy1 \
                            - orientation
                hist = np.histogram(angle_results, 8, (0, 360))[0]
                descriptor.append(hist)
        descriptor = np.array(descriptor).reshape(128)
        norm = np.sqrt((descriptor ** 2).sum())
        if int(norm):
            descriptor = descriptor / norm
            descriptors.append(descriptor)
            keypoints.append((x, y))
    return np.array(keypoints), np.array(descriptors).reshape(-1, 128)


if __name__ == '__main__':
    target = cv.imread('target.jpg', cv.IMREAD_GRAYSCALE)
    keypoints1, descriptors1 = sift(target)
    for i in range(1, 6):
        img = cv.imread('dataset/{}.jpg'.format(i), cv.IMREAD_GRAYSCALE)
        keypoints, descriptors = sift(img)
        matched_keypoints_in_target = []
        matched_keypoints_in_input = []
        for j in range(keypoints1.shape[0]):
            min_distance = 4
            second_min_distance = 4
            min_distance_keypoint = -1
            for k in range(keypoints.shape[0]):
                distance = np.sqrt(((descriptors1[j] - descriptors[k]) ** 2).sum())
                if distance < min_distance:
                    second_min_distance = min_distance
                    min_distance = distance
                    min_distance_keypoint = k

            if min_distance / second_min_distance < 0.8:
                matched_keypoints_in_target.append(keypoints1[j])
                matched_keypoints_in_input.append(min_distance_keypoint)

        print(i, len(matched_keypoints_in_target))
