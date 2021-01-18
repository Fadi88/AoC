import time
import math


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        method(*arg, **kw)
        print('Method ' + method.__name__ + ' took : ' +
              "{:2.5f}".format(time.time()-t) + ' sec')
    return wrapper_method


@profiler
def part1():

    import time


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        method(*arg, **kw)
        print('Method ' + method.__name__ + ' took : ' +
              "{:2.5f}".format(time.time()-t) + ' sec')
    return wrapper_method


@profiler
def part1():

    cnt = 0
    for l in open('input.txt'):
        p_list = l.strip().split()
        p_set = set(p_list)

        if len(p_list) == len(p_set):
            cnt += 1

    print(cnt)


@profiler
def part2():

    cnt = 0
    for l in open('input.txt'):
        p_list = []
        for p in l.strip().split():
            p = list(p)
            p.sort()
            p_list.append(''.join(p))

        p_set = set(p_list)

        if len(p_list) == len(p_set):
            cnt += 1

    print(cnt)


if __name__ == "__main__":

    part1()
    part2()
