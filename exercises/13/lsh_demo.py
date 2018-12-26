import numpy as np
import cv2 as cv


def feature_vector(img):
    half_height = img.shape[0] // 2
    half_width = img.shape[1] // 2
    # divide into 4 regions
    regions = (img[:half_height, :half_width], img[:half_height, half_width:],
               img[half_height:, :half_width], img[half_height:, half_width:])
    hists = []
    for r in regions:
        # sum of intensity of each color
        hist = np.array([r[:, :, i].sum() for i in range(3)], np.float64)
        hists.append(hist / hist.sum())
    v = np.concatenate(hists)
    for i in range(v.shape[0]):
        if v[i] < 0.3:
            v[i] = 0
        elif v[i] < 0.6:
            v[i] = 1
        else:
            v[i] = 2
    return v.astype(np.uint8)


def lsh(v, seg_map_set):
    """
    Locality Sensitive Hashing
    :param v: vector
    :param seg_map_set: segmented map set
    :return: int
    """
    result = ''
    for i, s in enumerate(seg_map_set):
        if len(s):
            # count elements in s that are less than v[i]
            count = 0
            for x in s:
                if x <= v[i]:
                    count += 1
                else:
                    break
            result += '1' * count + '0' * (len(s) - count)
    # represent the hash value as a decimal
    return int(result, 2)


class LSHTable:
    def __init__(self, map_sets, C, dim):
        self.C = C
        self.dim = dim
        self.map_sets = [self.segment_map_set(s) for s in map_sets]
        # Each dict is a hash bin.
        self.table = [dict() for _ in range(len(map_sets))]

    def segment_map_set(self, map_set):
        """
        Find I|1, I|2,... and return the result as a list
        :param map_set: I
        :return: list
        """
        j = 0
        segmented = []
        for i in range(self.dim):
            segment = []
            while j < len(map_set):
                if map_set[j] <= (i + 1) * self.C:
                    segment.append(map_set[j] - i * self.C)
                else:
                    break
                j += 1
            # An empty list is appended, like an empty set.
            segmented.append(segment)
        return segmented

    def add(self, v, data):
        """Add a vector to the hash table
        :param v: vector
        :param data: data associated with v
        """
        for i, s in enumerate(self.map_sets):
            h = lsh(v, s)
            if self.table[i].get(h) is None:
                self.table[i][h] = [(v, data)]
            else:
                self.table[i][h].append((v, data))

    def knn(self, v, k):
        """
        Find k nearest neighbors
        :param v: vector
        :param k: number of neighbors
        :return: list that contains filenames and Euclidean distances between
            the feature vector of this image and v
        """
        # Each element in candidates is a tuple: ((vector, data), distance)
        candidates = []
        for i, s in enumerate(self.map_sets):
            # for each vector in the same bin
            for c in self.table[i][lsh(v, s)]:
                # append to candidates if not a duplicate
                for appended_candidate in candidates:
                    # if both have the same filename
                    if c[1] == appended_candidate[0][1]:
                        break
                else:
                    # second item is the Euclidean distance
                    candidates.append((c, np.sqrt(np.square(v.astype(np.float64) - c[0]).sum())))
        candidates.sort(key=lambda c: c[1])
        # return a list of filenames
        if len(candidates) > k:
            return [(candidates[i][0][1], candidates[i][1]) for i in range(k)]
        else:
            return [(c[0][1], c[1]) for c in candidates]


if __name__ == '__main__':
    map_sets = [
        [2, 4, 11, 13, 16, 17, 23, 24], [1, 6, 13, 16, 18, 19, 21, 24],
        [1, 4, 12, 14, 16, 17, 19, 21], [2, 3, 5, 12, 14, 18, 21, 23],
        [3, 5, 6, 9, 13, 19, 20, 22]
    ]
    t = LSHTable(map_sets, 2, 12)
    directory = 'Dataset/'
    for i in range(1, 41):
        filename = str(i) + '.jpg'
        img = cv.imread(directory + filename)
        t.add(feature_vector(img), filename)
    img = cv.imread('target.jpg')
    v = feature_vector(img)
    print(t.knn(v, 8))
