"""Generate a graph to test the computation of PageRank"""

import random
from math import ceil

N_VERTICES = 1000
MAX_OUT_VERTICES = 100      # the maximum number of outgoing vertices
INITIAL_PAGERANK = 1
PARTITION_SIZE = 250
N_PARTS = ceil(N_VERTICES / PARTITION_SIZE)

if __name__ == '__main__':
    part = 1
    f = open('input/' + str(part) + '.txt', 'w')
    for i in range(N_VERTICES):
        if i >= part * PARTITION_SIZE:
            part += 1
            f.close()
            f = open('input/' + str(part) + '.txt', 'w')

        out_vertices = random.sample(range(N_VERTICES), random.randrange(MAX_OUT_VERTICES) + 1)
        out_vertices.sort()
        f.write(str(i) + '\t' + str(INITIAL_PAGERANK))
        for v in out_vertices:
            f.write(' ' + str(v))
        f.write('\n')
    f.close()
