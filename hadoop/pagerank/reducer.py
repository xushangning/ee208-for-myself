#!/usr/bin/python
import sys
import numpy as np

from generate_graph import N_VERTICES

if __name__ == '__main__':
    pageranks = np.zeros(N_VERTICES, np.float64)
    graph_structure = {}

    for line in sys.stdin:
        if line[0] == '|':
            try:    # detect whether the vertex has outgoing vertices
                vertex_id, out_vertices = line[1:].rstrip().split(' ', 1)
                # prepend a white space so that we don't need to care about
                # white space issues in output
                graph_structure[int(vertex_id)] = ' ' + out_vertices
            except ValueError:
                vertex_id = int(line.rstrip()[1:])
                graph_structure[vertex_id] = ''     # no outgoing vertices
        else:
            vertex_id, contributed_pagerank = line.rstrip().split('\t')
            vertex_id = int(vertex_id)
            contributed_pagerank = float(contributed_pagerank)
            pageranks[vertex_id] += contributed_pagerank

    for i in range(N_VERTICES):
        print(str(i) + '\t' + str(pageranks[i]) + graph_structure[i])
