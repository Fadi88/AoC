# pylint: disable=C0114,C0116,C0301,C0209,W1514,C0414,C0200

from time import time as perf_counter
from typing import Any
import os

input_file = os.path.join(os.path.dirname(__file__), "input.txt")
# input_file = os.path.join(os.path.dirname(__file__), "test.txt")


def profiler(method):
    def wrapper_method(*args: Any, **kwargs: Any) -> Any:
        t = perf_counter()
        ret = method(*args, **kwargs)
        print(f"Method {method.__name__} took : {perf_counter() - t:.3f} sec")
        return ret

    return wrapper_method


def is_valid(grid, nx, ny):
    return 0 <= nx < len(grid[0]) and 0 <= ny < len(grid)


def explore(grid, p):

    deltas = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    to_visit = [p]

    valid_path = 0
    nines = set()

    while to_visit:
        px, py = to_visit.pop(0)
        height = grid[py][px]

        if height == 9:
            valid_path += 1
            nines.add((px, py))
            continue

        for dx, dy in deltas:
            if is_valid(grid, px+dx, py+dy) and grid[py+dy][px+dx] == height + 1:
                to_visit.append((px+dx, py+dy))

    return valid_path, len(nines)


@profiler
def part_1():
    with open(input_file) as f:
        grid = list(list(map(int, l.strip())) for l in f)

    s = 0
    for y, l in enumerate(grid):
        for x, h in enumerate(l):
            if h == 0:
                _, n = explore(grid, (x, y))
                s += n

    print(s)


@profiler
def part_2():
    with open(input_file) as f:
        grid = list(list(map(int, l.strip())) for l in f)

    s = 0
    for y, l in enumerate(grid):
        for x, h in enumerate(l):
            if h == 0:
                u, _ = explore(grid, (x, y))
                s += u

    print(s)


if __name__ == "__main__":
    part_1()
    part_2()
