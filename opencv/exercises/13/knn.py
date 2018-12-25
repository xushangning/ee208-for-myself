import cv2 as cv

if __name__ == '__main__':
    orb = cv.ORB_create()
    bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)
    target = cv.imread('target.jpg')
    # preserve descriptors but discard keypoints
    _, target_des = orb.detectAndCompute(target, None)

    directory = 'Dataset/'
    dataset = []
    for i in range(1, 41):
        filename = str(i) + '.jpg'
        img = cv.imread(directory + filename)
        _, des = orb.detectAndCompute(img, None)
        matches = bf.match(des, target_des)
        # sort matches in the order of their distance
        matches.sort(key=lambda x: x.distance)

        # sum the distances of the 10 closest matches
        sum_of_distance = 0
        for j in range(5):
            sum_of_distance += matches[j].distance
        # each element in dataset is a tuple with format
        # (filename, sum of distance)
        dataset.append((filename, sum_of_distance))

    dataset.sort(key=lambda x: x[1])
    print(dataset[:8])
