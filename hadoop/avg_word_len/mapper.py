#!/usr/bin/python

import sys
import numpy as np
from string import ascii_letters

word_total_length = np.zeros(26, np.uint64)
word_count = np.zeros(26, np.uint32)

for line in sys.stdin:
    words = line.rstrip().split(' ')
    for w in words:
        if len(w) and w[0] in ascii_letters:
            index = ord(w[0].lower()) - 97
            try:
                word_total_length[index] += len(w)
            except IndexError as e:
                print(w[0])
                raise e
            word_count[index] += 1

for i in word_total_length:
    print(i, end=' ')
for i in word_count[:25]:       # leave out the last white space
    print(i, end=' ')
print(word_count[25])           # and replace it with a line feed
