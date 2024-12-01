# pylint: disable=C0114,C0116,C0301,C0209,W1514

from time import perf_counter
from collections import Counter


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
    l1, l2 = list(), list()
    for l in open("day01/input.txt"):
        p = l.strip().split()
        l1.append(int(p[0]))
        l2.append(int(p[1]))

    l1.sort()
    l2.sort()

    print(sum(abs(a - b) for a, b in zip(l1, l2)))

@profiler
def part2():
    l1, l2 = list(), list()
    for l in open("day01/input.txt"):
        p = l.strip().split()
        l1.append(int(p[0]))
        l2.append(int(p[1]))

    c = Counter(l2)

    print(sum(l * c[l] for l in l1))


if __name__ == "__main__":
    part1()
    part2()
