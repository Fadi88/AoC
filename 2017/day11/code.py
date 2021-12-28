import time
from collections import Counter


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        method(*arg, **kw)
        print(
            "Method "
            + method.__name__
            + " took : "
            + "{:2.5f}".format(time.time() - t)
            + " sec"
        )

    return wrapper_method


deltas = {
    "n": -1j,
    "s": 1j,
    "ne": 1,
    "nw": -1 - 1j,
    "se": 1 + 1j,
    "sw": -1,
}


@profiler
def part1():

    inp = open("day11/input.txt").read().split(",")

    pos = 0
    for d in inp:
        pos += deltas[d]

    print(int(abs(pos.imag) + (pos.real)))


@profiler
def part2():

    inp = open("day11/input.txt").read().split(",")

    pos = 0
    ds = []
    for d in inp:
        pos += deltas[d]
        ds.append(int(abs(pos.imag) + (pos.real)))

    print(max(ds))


if __name__ == "__main__":

    part1()
    part2()
