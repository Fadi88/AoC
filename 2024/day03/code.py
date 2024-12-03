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

def get_sum(input):
    pairs = re.findall(r"mul\((\d+),(\d+)\)", input)
    return sum(int(p[0]) * int(p[1]) for p in pairs)

@profiler
def part1():
    print(get_sum(open("day03/input.txt").read()))

@profiler
def part2():
    input = open("day03/input.txt").read()

    new_input = re.sub(r"don't\(\)[\s\S]*?do\(\)", "", input)

    print(get_sum(new_input))


if __name__ == "__main__":
    part1()
    part2()
