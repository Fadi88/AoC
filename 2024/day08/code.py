# pylint: disable=C0114,C0116,C0301,C0209,W1514,C0414

from time import time as perf_counter
from typing import Any
from collections import defaultdict
from itertools import combinations


def profiler(method):
    def wrapper_method(*args: Any, **kwargs: Any) -> Any:
        t = perf_counter()
        ret = method(*args, **kwargs)
        print(f"Method {method.__name__} took : {perf_counter() - t:.3f} sec")
        return ret

    return wrapper_method

def is_valid(p,max_x,max_y):
    return 0 <= p[0] < max_x and 0 <= p[1] < max_y
def generate_antinodes(p1,p2):
    # p1 - (p2 - p1)
    # p2 - (p1 - p2)

    np1 = p1[0] - (p2[0] - p1[0]), p1[1] - (p2[1] - p1[1])
    np2 = p2[0] - (p1[0] - p2[0]), p2[1] - (p1[1] - p2[1])

    return np1,np2

@profiler
def part1():
    antenas = defaultdict(set)
    with open("day08/input.txt") as f:
        for y, line in enumerate(f):
            for x, char in enumerate(line.strip()):
                if char != ".":
                    antenas[char].add((x, y))

            max_y = y + 1
            max_x = len(line.strip())

    antinodes = set()

    for a in antenas:
        for p in combinations(antenas[a], 2):
            p1 = p[0]
            p2 = p[1]

            np1,np2 = generate_antinodes(p1,p2)

            if is_valid(np1,max_x,max_y):
                antinodes.add(np1)
            if is_valid(np2,max_x,max_y):
                antinodes.add(np2)

    print(len(antinodes))

def generate_all_antinodes(p1,p2,max_x,max_y):
    antinodes = set()

    # return set of any grid position in line with p1 and p2
    x1,y1 = p1
    x2,y2 = p2

    for y3 in range(max_y):
        for x3 in range(max_x):
            if abs(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) == 0:
                antinodes.add((x3,y3))

    return antinodes

@profiler
def part2():
    antenas = defaultdict(set)
    with open("day08/input.txt") as f:
        for y, line in enumerate(f):
            for x, char in enumerate(line.strip()):
                if char != ".":
                    antenas[char].add((x, y))

            max_y = y + 1
            max_x = len(line.strip())

    antinodes = set()

    for a in antenas:
        for p in combinations(antenas[a], 2):
            antinodes |= generate_all_antinodes(p[0], p[1],max_x,max_y)

    print(len(antinodes))


if __name__ == "__main__":
    part1()
    part2()
