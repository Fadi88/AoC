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


def is_valid(grid, y, x):
    return 0 <= x < len(grid[0]) and 0 <= y < len(grid)


def check_xmas(grid, pos, d):
    px, py = pos[0], pos[1]
    dx, dy = d[0], d[1]

    return all(is_valid(grid, py+dy*(1+i), px+dx*(1+i)) and
               grid[py + dy*(1+i)][px+dx*(1+i)] == c
               for i, c in enumerate("MAS"))


@profiler
def part1():
    grid = [list(l.strip()) for l in open("day04/input.txt")]

    s = 0
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == "X":
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == dy == 0:
                            continue
                        s += check_xmas(grid, (x, y), (dx, dy))
    print(s)


def check_xmas_2(grid, x, y):
    if not all(is_valid(grid, y+dy, x+dx) for dx in [-1, 1] for dy in [-1, 1]):
        return False

    chars = [grid[y+1][x+1], grid[y-1][x-1], grid[y-1][x+1], grid[y+1][x-1]]

    return chars.count("S") == 2 and chars.count("M") == 2 and chars[0] != chars[1]


@profiler
def part2():
    grid = [list(l.strip()) for l in open("day04/input.txt")]

    s = 0
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == "A":
                s += check_xmas_2(grid, x, y)
    print(s)


if __name__ == "__main__":
    part1()
    part2()
