import time
import re
from itertools import combinations
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

    with open('input.txt') as f:
        inp = [*map(int, f.read().split())]

    cnt = 0
    for i in range(len(inp)):
        for c in combinations(inp, i+1):
            if sum(c) == 150:
                cnt += 1

    print(cnt)


@profiler
def part2():

    with open('input.txt') as f:
        inp = [*map(int, f.read().split())]

    cnt = defaultdict(int)

    for i in range(len(inp)):
        for c in combinations(inp, i+1):
            if sum(c) == 150:
                cnt[i+1] += 1

        if len(cnt) > 1:
            break

    print(cnt[min(cnt.keys())])


if __name__ == "__main__":

    part1()
    part2()
