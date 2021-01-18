import time
import os
from itertools import permutations


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        method(*arg, **kw)
        print('Method ' + method.__name__ + ' took : ' +
              "{:2.5f}".format(time.time()-t) + ' sec')
    return wrapper_method


@profiler
def part1():

    inp = []
    for l in open('input.txt').read().split('\n'):
        inp.append([*map(int, l.split())])

    total = 0
    for l in inp:
        total += max(l) - min(l)

    print(total)


@profiler
def part2():

    inp = []
    for l in open('input.txt').read().split('\n'):
        inp.append([*map(int, l.split())])

    total = 0
    for l in inp:
        for p in permutations(l, 2):
            if p[0] % p[1] == 0:
                total += p[0] // p[1]
                break
    print(total)


if __name__ == "__main__":

    part1()
    part2()
