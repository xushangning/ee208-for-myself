#!/usr/bin/python
import sys

from generate_graph import N_VERTICES

ALPHA = 0.2

if __name__ == '__main__':
    for line in sys.stdin:
        vertex_id, rest = line.rstrip().split('\t', 1)
        try:    # detect whether the vertex has out vertices
            pagerank, out_vertices = rest.split(' ', 1)
            # output the outgoing vertices of the vertex
            print('|' + vertex_id, out_vertices)
            pagerank = float(pagerank)
            out_vertices = [int(x) for x in out_vertices.split(' ')]
            n_out_vertices = len(out_vertices)

            # split PageRank from teleporting to the all the webpages
            contributing_pagerank = pagerank * (1 - ALPHA) / n_out_vertices
            teleport_pagerank = pagerank * ALPHA / N_VERTICES
            j = 0
            for i in range(N_VERTICES):
                if i < out_vertices[j]:
                    print(str(i) + '\t' + str(teleport_pagerank))
                elif i == out_vertices[j]:
                    print(str(i) + '\t' + str(contributing_pagerank + teleport_pagerank))
                    if j == n_out_vertices - 1:
                        out_vertices[-1] = N_VERTICES
                    else:
                        j += 1
        except ValueError:  # This vertex don't have outgoing vertices,
            # so its PageRank will be split among all webpages for teleporting.
            # output the outgoing vertices of the vertex (there are none)
            print('|' + vertex_id)
            pagerank = float(rest)
            teleport_pagerank = 1 / N_VERTICES
            # output PageRank contributed by teleporting
            for i in range(N_VERTICES):
                print(str(i) + '\t' + str(teleport_pagerank))
