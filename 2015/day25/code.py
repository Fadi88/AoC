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

    a1 = 20151125
    fac = 252533
    div = 33554393
    # input
    row = 2981
    column = 3075

    n = (row + column - 1)*(row + column - 2)//2 + column -1
    print((a1* pow(fac,n,div))%div)


if __name__ == "__main__":

    part1()
