# pylint: disable=C0114,C0116,C0301,C0209,W1514

from time import perf_counter
from functools import cache


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print("Method " + method.__name__ + " took : " + "{:2.5f}".format(perf_counter() - t) + " sec")
        return ret

    return wrapper_method


def get_number(grid, c_p, c_d):
    steps = {">": (+1, 0), "<": (-1, 0), "^": (0, -1), "v": (0, +1)}
    mirrors = {"/": {"^": ">", "v": "<", "<": "v", ">": "^"}, "\\": {"^": "<", "v": ">", "<": "^", ">": "v"}}
    to_visit = [(c_d, c_p)]
    energized = set()

    while to_visit:
        c_d, c_p = to_visit.pop(0)

        if (c_d, c_p) in energized:
            continue

        if 0 <= c_p[0] < len(grid[0]) and 0 <= c_p[1] < len(grid):
            energized.add((c_d, c_p))
            if grid[c_p[1]][c_p[0]] == "|" and c_d in "<>":
                to_visit.append(("v", c_p))
                to_visit.append(("^", c_p))
                continue
            elif grid[c_p[1]][c_p[0]] == "-" and c_d in "v^":
                to_visit.append((">", c_p))
                to_visit.append(("<", c_p))
                continue
            elif grid[c_p[1]][c_p[0]] in mirrors:
                c_d = mirrors[grid[c_p[1]][c_p[0]]][c_d]
            d = steps[c_d]
            c_p = (c_p[0] + d[0], c_p[1] + d[1])
            to_visit.append((c_d, c_p))
    return len(set(p[1] for p in energized))


@profiler
def part1():
    grid = [list(l.strip()) for l in open("day16/input.txt")]
    print(get_number(grid, (0, 0), ">"))


@profiler
def part2():
    grid = [list(l.strip()) for l in open("day16/input.txt")]

    acc = []
    for x in range(len(grid[0])):
        acc.append(get_number(grid, (x, 0), "v"))
        acc.append(get_number(grid, (x, len(grid) - 1), "^"))

    for y in range(len(grid[0])):
        acc.append(get_number(grid, (0, y), ">"))
        acc.append(get_number(grid, (x, len(grid[0]) - 1), "<"))

    print(max(acc))


if __name__ == "__main__":
    part1()
    part2()
