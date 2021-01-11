import time
import os
from collections import Counter


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        method(*arg, **kw)
        print('Method ' + method.__name__ + ' took : ' +
              "{:2.5f}".format(time.time()-t) + ' sec')
    return wrapper_method


@profiler
def part1():

    with open('input.txt') as f:
        inp = f.read().split('\n')

    table = []
    for i in range(len(inp[0])):
        t = Counter([l[i] for l in inp])
        table.append(t.most_common()[0][0])

    print(''.join(table))


@profiler
def part2():

    with open('input.txt') as f:
        inp = f.read().split('\n')

    table = []
    for i in range(len(inp[0])):
        t = Counter([l[i] for l in inp])
        table.append(t.most_common()[-1][0])

    print(''.join(table))


if __name__ == "__main__":

    part1()
    part2()
