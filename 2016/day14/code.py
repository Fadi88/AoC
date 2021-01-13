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


cache = {}


def get_md5(st):
    global cache

    if st in cache:
        hash = cache[st]
    else:
        hash = hashlib.md5(bytes(st, 'utf-8')).hexdigest()
        cache[st] = hash

    return hash


@profiler
def part1():

    salt = 'qzyelonm'
    idx = 0

    f_idx = []

    while len(f_idx) < 64:

        st = salt+str(idx)

        h = get_md5(st)
        if re.match(r'\w*(\w)\1{2}\w*', h) is not None:
            ch = re.match(r'\w*(\w)\1{2}\w*', h)[1]
            for i in range(1, 1001):
                new_h = get_md5(salt+str(idx+i))
                if re.match('\w*'+ch+'{5}\w*', new_h) is not None:
                    f_idx.append(idx)
                    break

        idx += 1

    print(f_idx[-1])


cache_2016 = {}


def get_md5_rec(st, h='', cnt=0):
    global cache_2016

    if cnt == 0:
        h = st

    k = h+'_'+str(cnt)

    if k in cache_2016:
        return cache_2016[k]

    if cnt == 2016:
        cache_2016[k] = get_md5(h)
        return cache_2016[k]
    else:
        cache_2016[k] = get_md5_rec(st, get_md5(h), cnt+1)
        return cache_2016[k]


@profiler
def part2():

    salt = 'qzyelonm'
    idx = 1

    f_idx = []
    sys.setrecursionlimit(2016)

    while len(f_idx) < 65:

        st = salt+str(idx)

        h = get_md5_rec(st)
        if re.match(r'\w*(\w)\1{2}\w*', h) is not None:
            ch = re.match(r'\w*(\w)\1{2}\w*', h)[1]
            for i in range(1, 1001):
                new_h = get_md5_rec(salt+str(idx+i))
                if re.match(r'\w*'+ch+r'{5}\w*', new_h) is not None:
                    f_idx.append(idx)
                    break

        idx += 1

    print(f_idx[-1])


if __name__ == "__main__":

    part1()
    part2()
