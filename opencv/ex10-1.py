import matplotlib.pyplot as plt
import cv2 as cv

for count in range(2):
    plt.subplot(2, 1, count + 1)    # create subplots
    filename = 'img{}.png'.format(count + 1)
    plt.title('Color Histogram of ' + filename)
    # read the image
    img = cv.imread('../instructions/10/images/' + filename, cv.IMREAD_COLOR)
    n_pixels = img.size // 3    # the number of pixels in the image
    color = ('b', 'g', 'r')     # colours used in plotting
    for i, c in enumerate(color):
        # find and normalised the histogram
        hist = cv.calcHist([img], [i], None, [256], [0, 256]) / n_pixels
        plt.plot(hist, c)
plt.tight_layout()      # automatically adjust spacing between axes and titles
plt.savefig('colour_hist.png')
