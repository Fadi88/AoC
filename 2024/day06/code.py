# pylint: disable=C0114,C0116,C0301,C0209,W1514

from time import perf_counter
from collections import defaultdict


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print(
            "Method "
            + method.__name__
            + " took : "
            + "{:2.5f}".format(perf_counter() - t)
            + " sec"
        )
        return ret

    return wrapper_method


@profiler
def part1():
    ps = open("day06/input.txt").read()


@profiler
def part2():
    ps = open("day06/input.txt").read()


if __name__ == "__main__":
    part1()
    part2()
