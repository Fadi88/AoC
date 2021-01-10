import random
import time
import re
from itertools import combinations
from operator import mul
from functools import reduce


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print('Method ' + method.__name__ + ' took : ' +
              "{:2.5f}".format(time.time()-t) + ' sec')
        return ret
    return wrapper_method


@profiler
def part1():

    vals = [int(l) for l in open('input.txt').read().split('\n')]
    w = sum(vals)//3
    grps = []
    for i in range(1, len(vals)):
        grps += [reduce(mul, grp)
                 for grp in combinations(vals, i) if sum(grp) == w]

    print(min(grps))


@profiler
def part2():

    vals = [int(l) for l in open('input.txt').read().split('\n')]
    w = sum(vals)//4
    grps = []
    for i in range(1, len(vals)):
        grps += [reduce(mul, grp)
                 for grp in combinations(vals, i) if sum(grp) == w]

    print(min(grps))


if __name__ == "__main__":

    part1()
    part2()
