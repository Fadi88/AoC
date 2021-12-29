import time
from collections import Counter


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print(
            "Method "
            + method.__name__
            + " took : "
            + "{:2.5f}".format(time.time() - t)
            + " sec"
        )
        return ret

    return wrapper_method


@profiler
def part1():

    vals = [int(l.split(" ")[-1]) for l in open("day15/input.txt").read().split("\n")]

    rem = 2147483647
    factors = [16807, 48271]

    cnt = 0
    for _ in range(int(4e7 + 1)):
        vals[0] = vals[0] * factors[0] % rem
        vals[1] = vals[1] * factors[1] % rem

        if vals[0] & 0xFFFF == vals[1] & 0xFFFF:
            cnt += 1

    print(cnt)


@profiler
def part2():

    vals = [int(l.split(" ")[-1]) for l in open("day15/input.txt").read().split("\n")]

    rem = 2147483647
    factors = [16807, 48271]

    cnt = 0
    for _ in range(int(5e6 + 1)):
        while True:
            vals[0] = vals[0] * factors[0] % rem
            if vals[0] % 4 == 0:
                break

        while True:
            vals[1] = vals[1] * factors[1] % rem
            if vals[1] % 8 == 0:
                break

        if vals[0] & 0xFFFF == vals[1] & 0xFFFF:
            cnt += 1

    print(cnt)


if __name__ == "__main__":

    part1()
    part2()
