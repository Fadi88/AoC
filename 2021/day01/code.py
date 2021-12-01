import time
import os


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
    l = [int(l) for l in open('input.txt')]
    cnt = 0
    for i in range(1, len(l)):
        if l[i] > l[i-1]:
            cnt += 1

    print("part 1 ", cnt)


@profiler
def part2():
    l = [int(l) for l in open('input.txt')]

    cnt = 0
    for i in range(2, len(l)-1):
        if l[i + 1] > l[i - 2]:
            cnt += 1

    print("part 2 ", cnt)


if __name__ == "__main__":

    part1()
    part2()
