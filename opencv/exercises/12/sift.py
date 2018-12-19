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

    dy = img[2:, 1:-1].astype(np.int32) - img[:-2, 1:-1]
    dx = img[1:-1, 2:].astype(np.int32) - img[1:-1, :-2]
    # if the image is m * n, the mags and angles array are (m - 2) * (n - 2)
    mags = np.sqrt(dx * dx + dy * dy)
    angles = np.rad2deg(np.arctan2(dy, dx))
    # convert angle representation from (-180, 180] to [0, 360)
    angles += (angles < 0).astype(np.int16) * 360
    # find orientation for each keypoint
    keypoints_with_orientation = []
    for x, y in keypoints:
        x = int(x)
        y = int(y)
        # if the neighborhood sits next to the border
        if x < 3 or x + 3 > img.shape[0] or y < 3 or y + 3 > img.shape[1]:
            continue

        # draw a 5 * 5 window on magnitudes and gradients
        # Indices are offset by 1.
        mag_part = mags[y - 3: y + 2, x - 3: x + 2]
        angle_part = angles[y - 3: y + 2, x - 3: x + 2]
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
                # store interpolated angles
                angle_results = np.zeros((4, 4))
                # for each angle to interpolate
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
        matches_img = np.zeros((max(target.shape[0], img.shape[0]),
                                target.shape[1] + img.shape[1]), np.uint8)
        matches_img[:target.shape[0], :target.shape[1]] = target
        matches_img[:img.shape[0], target.shape[1]:] = img
        n_keypoint = 0
        for j in range(keypoints1.shape[0]):
            min_distance = 4
            second_min_distance = 4
            m = -1      # index for keypoint in img with minimum distance
            for k in range(keypoints.shape[0]):
                distance = np.sqrt(((descriptors1[j] - descriptors[k]) ** 2).sum())
                print(k, distance)
                if distance < min_distance:
                    second_min_distance = min_distance
                    min_distance = distance
                    m = k

            if n_keypoint > 10:
                break

            if min_distance / second_min_distance < 0.8:
                # print(n_keypoint)
                # print(descriptors1[j])
                # print(descriptors[m])
                keypoint_in_img = (keypoints[m][0] + target.shape[0], keypoints[m][1])
                keypoint_in_target = (keypoints1[j][0], keypoints1[j][1])
                cv.circle(matches_img, keypoint_in_target, 5, 240)
                cv.circle(matches_img, keypoint_in_img, 5, 240)
                cv.line(matches_img, keypoint_in_target, keypoint_in_img, 240)
            n_keypoint += 1

        cv.imwrite('matches.png', matches_img)
