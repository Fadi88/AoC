import time
from functools import reduce


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


def reverse_section(circle, pos, l):
    for i in range(l // 2):
        tmp = circle[(pos + i) % len(circle)]
        circle[(pos + i) % len(circle)] = circle[(pos + l - i - 1) % len(circle)]
        circle[(pos + l - i - 1) % len(circle)] = tmp


@profiler
def part1():

    inp = list(map(int, open("day10/input.txt").read().split(",")))
    circle = list(range(256))

    skip = 0
    pos = 0

    for n in inp:
        reverse_section(circle, pos, n)

        pos = (pos + n + skip) % len(circle)

        skip += 1

    print(circle[0] * circle[1])


@profiler
def part2():

    inp = list(map(ord, open("day10/input.txt").read()))
    inp += [17, 31, 73, 47, 23]

    circle = list(range(256))

    skip = 0
    pos = 0

    for _ in range(64):
        for n in inp:
            reverse_section(circle, pos, n)

            pos = (pos + n + skip) % len(circle)

            skip += 1

    dense_hash = [reduce(lambda a, b: a ^ b, circle[i * 16 + 0 : i * 16 + 16]) for i in range(16)]


    print("".join(map(lambda d: hex(d)[2:].zfill(2), dense_hash)))


if __name__ == "__main__":

    part1()
    part2()
