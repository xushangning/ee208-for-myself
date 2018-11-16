#!/usr/bin/python

import sys
import numpy as np

word_total_length = np.zeros(26, np.uint64)
word_count = np.zeros(26, np.uint32)

for line in sys.stdin:
    data = [int(n) for n in line.rstrip().split(' ')]
    word_total_length += np.array(data[:26], dtype=np.uint64)
    word_count += np.array(data[26:], dtype=np.uint32)

for i in range(26):
    if word_count[i]:
        print(chr(i + 97), word_total_length[i] / word_count[i])
