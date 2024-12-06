import time
import re
import hashlib
import sys


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print('Method ' + method.__name__ + ' took : ' +
              "{:2.5f}".format(time.time()-t) + ' sec')
        return ret
    return wrapper_method


def get_nums(l):
    ps = l.strip().split()
    return (int(ps[3]), int(ps[-1][:-1]))


@profiler
def part_1():
    inp = [get_nums(l) for l in open('day15/input.txt').readlines()]

    time = 0
    while not all((time + i + disc[1]) % disc[0] == 0 for i, disc in enumerate(inp)):
        time += 1

    print(time-1)

@profiler
def part_2():
    inp = [get_nums(l) for l in open('day15/input.txt').readlines()]
    inp.append((11, 0)) 

    time = 0
    while not all((time + i + disc[1]) % disc[0] == 0 for i, disc in enumerate(inp)):
        time += 1

    print(time-1)

if __name__ == "__main__":

    part_1()
    part_2()
