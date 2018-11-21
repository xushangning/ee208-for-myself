#!/usr/bin/python
"""Repeatedly run MapReduce to compute PageRank"""

from subprocess import run

if __name__ == '__main__':
    N_ITERATIONS = 20
    HADOOP_COMMAND = 'hadoop jar /usr/lib/hadoop-3.1.1/share/hadoop/tools/' \
                     'lib/hadoop-streaming-3.1.1.jar ' \
                     '-files mapper.py,reducer.py -mapper mapper.py ' \
                     '-reducer reducer.py'.split(' ')
    RM = 'hdfs dfs -rm'.split(' ')

    input_dir = 'input'
    for i in range(N_ITERATIONS):
        output_dir = 'output_' + str(i)
        run(HADOOP_COMMAND + ['-input', input_dir, '-output', output_dir])
        run(RM + [output_dir + '/_SUCCESS'])

        input_dir = output_dir
