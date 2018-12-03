import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv

OUTPUT_FOLDER_NAME = 'canny_output'


def canny(img, t1, t2):
    """Detect edges with the Canny edge detector
    :param img: numpy.ndarray: the input grayscale image
    :param t1: float: threshold 1
    :param t2: float: threshold 2
    """
    dx = cv.Sobel(img, cv.CV_32F, 2, 0)
    dy = cv.Sobel(img, cv.CV_32F, 0, 2)
    mag = np.sqrt(dx * dx + dy * dy)
    ang = np.arctan(dy, dx)

    # draw a mesh about gradients
    plt.contourf(np.flip(mag, 0))
    plt.colorbar()
    plt.savefig(OUTPUT_FOLDER_NAME + '/1_gradient_mesh.png')

    # classify gradient into two categories by their directions: 1 for vertical
    # and 0 for horizontal
    ang_directions = np.zeros(ang.shape, np.bool)
    # Gradients with angles not less than pi/4 or not greater than -pi/4 are
    # regarded as vertical.
    ang_directions[ang >= np.pi / 4] = True
    ang_directions[ang <= - np.pi / 4] = True

    edges = np.zeros(img.shape, np.uint8)
    # Non-maximum suppression
    suppressed_mag = np.copy(mag)
    for i in range(1, mag.shape[0] - 1):
        for j in range(1, mag.shape[1] - 1):
            if ang_directions[i][j]:
                # intensity at (i, j) is not greater than its neighbors in
                # vertical direction
                if mag[i][j] <= mag[i + 1][j] or mag[i][j] <= mag[i - 1][j]:
                    suppressed_mag[i][j] = 0
            elif mag[i][j] <= mag[i][j + 1] or mag[i][j] <= mag[i][j - 1]:
                    suppressed_mag[i][j] = 0
    mag = suppressed_mag
    plt.contourf(np.flip(mag, 0))
    plt.savefig(OUTPUT_FOLDER_NAME + '/1_gradient_mesh_post_suppression.png')

    # double thresholds
    edges[mag >= t2] = 255
    cv.imwrite(OUTPUT_FOLDER_NAME + '/1_2t.png', edges)

    OFFSETS = np.array(((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1),
                        (1, 0), (1, 1)), np.int8)
    # hysteresis
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if mag[i][j] >= t1:
                for offset_i, offset_j in OFFSETS:
                    i_ = i + offset_i
                    j_ = j + offset_j
                    if i_ >= 0 and j_ >= 0 and i_ < img.shape[0] and j_ < img.shape[1]:
                        if mag[i_][j_] >= t2:
                            edges[i][j] = 255
                            break
    return edges


if __name__ == '__main__':
    img = cv.imread('1.jpg', cv.IMREAD_GRAYSCALE)
    cv.imwrite(OUTPUT_FOLDER_NAME + '/1_final.png', canny(img, 20, 60))
    cv.imwrite(OUTPUT_FOLDER_NAME + '/1_built_in.png', cv.Canny(img, 10, 60))
