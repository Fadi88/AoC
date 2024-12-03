# pylint: disable=C0114,C0116,C0301,C0209,W1514

from time import perf_counter
import re


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
    input = open("day03/input.txt").read()
    pairs = re.findall(r"mul\((\d+),(\d+)\)", input)
    print(sum(int(p[0]) * int(p[1]) for p in pairs))


def get_sum(e):
    if "do()" in e:
        pairs = re.findall(r"mul\((\d+),(\d+)\)", e.split("do()", maxsplit=1)[1])
        return sum(int(p[0]) * int(p[1]) for p in pairs)

    return 0


@profiler
def part2():
    input = open("day03/input.txt").read()

    #input = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"

    enables = input.split("don't()")

    enables[0] = "do()" + enables[0]

    print(sum(get_sum(e) for e in enables))


if __name__ == "__main__":
    part1()
    part2()
