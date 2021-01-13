import time
import re
from collections import defaultdict


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

    plan = []

    for l in open('input.txt').read().split('\n'):
        plan.append(l.count(',')+1)

    print(sum(2 * sum(plan[:f]) - 3 for f in range(1, 4)))


@profiler
def part2():

    plan = []

    for l in open('input.txt').read().split('\n'):
        plan.append(l.count(',')+1)

    plan[0] += 4

    print(sum(2 * sum(plan[:f]) - 3 for f in range(1, 4)))


if __name__ == "__main__":

    part1()
    part2()
