import numpy as np


def lsh(v, C, seg_map_set):
    """
    Locality Sensitive Hashing
    :param v: vector
    :param C: code length
    :param seg_map_set: segmented map set
    :return: int
    """
    result = ''
    for i, s in enumerate(seg_map_set):
        if len(s):
            count = 0
            for x in s:
                if x <= v[i]:
                    count += 1
                else:
                    break
            result += '1' * count + '0' * (len(s) - count)
    return int(result, 2)


class LSHTable:
    def __init__(self, map_sets, C, dim):
        self.C = C
        self.dim = dim
        self.table = []
        print(self.segment_map_set(map_sets))

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
            segmented.append(segment)
        return segmented


if __name__ == '__main__':
    # p = np.array([2, 4, 3, 5], np.uint8)
    # I = [[1, 2, 3, 5], [2, 3], [], []]
    # C = 5
    # print(lsh(p, C, I))
    t = LSHTable([1, 2, 3, 5, 7, 8], 5, 4)
