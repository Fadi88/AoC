# pylint: disable=C0114,C0116,C0301,C0209,W1514

from time import perf_counter
from functools import cache
import re


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print("Method " + method.__name__ + " took : " + "{:2.5f}".format(perf_counter() - t) + " sec")
        return ret

    return wrapper_method


@cache
def get_hash(st):
    hash_res = 0
    for c in st:
        hash_res += ord(c)
        hash_res *= 17
        hash_res %= 256

    return hash_res


@profiler
def part1():
    print(sum(map(get_hash, open("day15/input.txt").read().split(","))))


@profiler
def part2():
    seq = open("day15/input.txt").read().split(",")

    boxes = [{} for _ in range(256)]

    for s in seq:
        label = re.findall(r"\w+", s)[0]
        box = get_hash(label)
        op = s.replace(label, "")

        match op[0]:
            case "-":
                if label in boxes[box]:
                    del boxes[box][label]
            case "=":
                boxes[box][label] = int(op[-1])

    print(sum((i + 1) * (l + 1) * (boxes[i][b]) for i in range(256) for l, b in enumerate((boxes[i]))))


if __name__ == "__main__":
    part1()
    part2()
