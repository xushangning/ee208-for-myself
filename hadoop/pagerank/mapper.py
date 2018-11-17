import numpy as np


def construct_adj_matrix():
    """
    Construct an adjacency matrix from input in the form
        <id>\t<next_id1> <next_id2> ...
    :return: numpy.ndarray an adjacency matrix
    """
    n = int(input())    # the dimension of the adjacency matrix
    adj_m = np.zeros((n, n), np.int8)
    for _ in range(n):
        line = input()
        vertex_id, line = line.split('\t', 1)
        vertex_id = int(vertex_id) - 1
        for next_id in (int(x) - 1 for x in line.split(' ')):
            adj_m[vertex_id][next_id] = 1
    return adj_m


def pagerank(alpha, adj_m, n_iter):
    """
    Calculate PageRank for a graph specified in an n * n adjacency matrix.
    :param alpha: float the teleport probability
    :param adj_m: numpy.ndarray an n * n adjacency matrix
    :param n_iter: int the number of iterations
    :return: numpy.ndarray an n * 1 vector
    """
    n = adj_m.shape[0]
    tpm = np.array(adj_m, np.float64)     # transition probability matrix
    result = np.zeros(n)
    result[0] = 1

    # construct the transition probability matrix for PageRank
    for i in range(len(tpm)):
        n_nonzero_entries = np.count_nonzero(tpm[i])
        if n_nonzero_entries:
            tpm[i] *= (1 - alpha) / n_nonzero_entries
            tpm[i] += alpha / n
        else:
            tpm[i] = np.full(n, 1 / n)

    for i in range(n_iter):
        result = result @ tpm
        print(result)
    return result


if __name__ == '__main__':
    adj_m = construct_adj_matrix()
    n_iter = int(input())   # the number of iterations to run PageRank
    pagerank(0.5, adj_m, n_iter)
