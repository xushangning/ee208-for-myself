from Bitarray import Bitarray
from GeneralHashFunctions import *


class BloomFilter:
    def __init__(self, n_bit, *hash_func):
        """
        :param n_bit: number of bits in the bit array
        :param hash_func: list of hash functions to use
        """
        self.n_bit = n_bit
        self.hash_func = hash_func
        self.bit_array = Bitarray(self.n_bit)
        # save all added keywords
        # acts as ground truth in calculating the false positive rate
        self.added_keywords = set()
        self.n_false_positives = 0  # number of false positives
        # number of keywords that have not been added to the filter
        # and are determined to not have been added
        self.n_true_negatives = 0

    def set(self, keyword):
        """
        Set corresponding bits specified by hashing the keyword
        :param keyword: string
        """
        self.added_keywords.add(keyword)
        for hash_f in self.hash_func:
            self.bit_array.set(hash_f(keyword) % self.bit_array.size)

    def query(self, keyword):
        """
        Determine whether a keyword has been added to the Bloom Filter
        :param keyword: string
        :return: bool
        """
        for hash_f in self.hash_func:
            # if the bit specified by the hash is not set
            if not self.bit_array.get(hash_f(keyword) % self.bit_array.size):
                self.n_true_negatives += 1
                return False    # keyword hasn't been added to the filter
        if keyword not in self.added_keywords:
            self.n_false_positives += 1
        return True     # all bits are set, keyword may have been added

    def false_positive_rate(self):
        """
        Return the false positive rate as of now.
        :return: float
        """
        return self.n_false_positives / (
                self.n_false_positives + self.n_true_negatives)

    def print_stats(self):
        """
        Statistics about the filter
        """
        print("Number of Added Keywords:", len(self.added_keywords))
        print("Number of False Positives:", self.n_false_positives)
        print("Number of True Negatives:", self.n_true_negatives)
        print("False Positive Rate:", self.false_positive_rate())


# Test the false positive rate with pg1661.txt
if __name__ == "__main__":
    BIT_ARRAY_SIZE = 131072
    my_filter = BloomFilter(
        BIT_ARRAY_SIZE,
        RSHash,
        hash,
        JSHash,
        SDBMHash,
        FNVHash
    )
    with open('code/pg1661.txt', 'r') as f:
        for line in f:
            for word in line.strip().split(' '):
                if not my_filter.query(word):
                    my_filter.set(word)
    print(my_filter.false_positive_rate())
    print(len(my_filter.added_keywords))
