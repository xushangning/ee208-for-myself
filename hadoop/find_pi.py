"""Increase the number of samples by a decade until a desirable precision in
computing π is achieved"""

import subprocess

f = open('mini_ex.csv', 'w')

f.write('Number of samples,Time,Value of approximation\n')
for i in range(20):
    power = 10 ** (i + 1)   # used as number of samples
    cp = subprocess.run(
        (
            'hadoop', 'jar',
            '/usr/lib/hadoop-3.1.1/share/hadoop/mapreduce/'
            'hadoop-mapreduce-examples-3.1.1.jar',
            'pi', '5', str(power)
        ),
        capture_output=True,
        encoding='UTF-8'
    )
    # select two lines to extract the time and calculated value
    results = cp.stdout.split('\n')[-3:-1]
    # The following two comment lines are sample output:
    # Job Finished in 1.653 seconds
    # Estimated value of Pi is 3.80000000000000000000
    pi_str = results[1].split(' ')[-1]
    pi = float(pi_str)
    # split the first line in white space and extract the third element
    # i.e. the running time
    f.write(str(power) + ',' + results[0].split(' ')[3] + ',' + pi_str + '\n')
    print(power)

    if abs(pi - 3.14159) < 0.00001:
        break

f.close()
