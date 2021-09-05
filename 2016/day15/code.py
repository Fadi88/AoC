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


if __name__ == "__main__":

    inp = []
    for l in open('input.txt'):
        p = l.strip().split()
        inp.append([int(p[3]), int(p[-1][:-1])])

    m = [l[0] for l in inp]
    r = [(l[0] - l[1] - (idx + 1))%l[0] for idx,l in enumerate(inp)]

    # https://www.dcode.fr/restes-chinois
    for p in zip(r , m):
        print(*p)

