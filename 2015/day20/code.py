import time
import re
from collections import defaultdict
from functools import reduce


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print('Method ' + method.__name__ + ' took : ' +
              "{:2.5f}".format(time.time()-t) + ' sec')
        return ret
    return wrapper_method


def fac(n):
    return set(reduce(list.__add__, 
                ([i, int(n//i)] for i in range(1, int(n**0.5) + 1) if n % i == 0)))


@profiler
def part1():

    inp = 36000000

    for i in range(100000,1000000):
        if sum(fac(i)) * 10 >= inp :
            print(i)
            break


@profiler
def part2():

    inp = 36000000

    for i in range(100000,1000000):
        l = list(fac(i))
        l.sort()
        if sum(e for e in l if i//e < 50) * 11 >= inp:
            print(i)
            break

if __name__ == "__main__":

    part1()
    part2()

