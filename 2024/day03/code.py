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
    print(sum( int(p[0]) * int(p[1]) for p in pairs))




@profiler
def part2():
    input = open("day03/input.txt").read()

    #input = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"

    enables = input.split("don't()")

    s = 0
    for e in enables:
        if "do()" in e:
            pairs = re.findall(r"mul\((\d+),(\d+)\)", e.split("do()",maxsplit=1)[1])
            s += sum( int(p[0]) * int(p[1]) for p in pairs)
        if enables.index(e) == 0:
            pairs = re.findall(r"mul\((\d+),(\d+)\)", e)
            s += sum( int(p[0]) * int(p[1]) for p in pairs)

    print(s)
   

if __name__ == "__main__":
    part1()
    part2()


