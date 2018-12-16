#!/usr/bin/python
import numpy as np
import sys

n_trials = 1000000


def parse_roll(str_in):
    str_in = str_in.lower()
    if 'd' in str_in:
        n, d = [int(s) for s in str_in.split('d')]
        results = np.random.randint(low=1, high=d+1, size=(n_trials, n))
        mean = n * 0.5 * (d+1)
        return results[0].sum(), str(results[0]), mean, results.sum(axis=1)
    else:
        return int(str_in), '{:s}'.format(str_in), int(str_in), np.ones(n_trials)*int(str_in)

    
def roll():
    args = sys.argv[1:]
    message1 = "= "
    message2 = ""
    total = 0
    means = 0
    distribution = np.zeros(n_trials)
    for arg in args:
        if arg == '+':
            message1 += ' + '
            message2 += ' + '
        else:
            the_sum, rolls, mean, realizations = parse_roll(arg)
            message1 += str(the_sum) + ' '*(len(rolls) - len(str(the_sum)))
            message2 += rolls
            total += the_sum
            means += mean
            distribution += realizations
    print('*************')
    print('Total: {:4d}'.format(total))
    print('*************')
    print(message1)
    print(message2)
    print('Mean: {:.1f}'.format(means))
    print('Percentile: {:.1f}%'.format((total > distribution).mean()*100.))


if __name__ == '__main__':
    roll()
