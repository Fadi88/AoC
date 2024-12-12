# pylint: disable=C0114,C0116,C0301,C0209,W1514,C0414

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


def is_valid(p, max_x, max_y):
    x, y = p
    return 0 <= x < max_x and 0 <= y < max_y


def flood_fill(grid, p):

    max_x, max_y = len(grid[0]), len(grid)

    start_x, start_y = p
    crop = grid[start_y][start_x]

    visited = set()
    to_visit = [p]

    while to_visit:
        x, y = to_visit.pop()
        visited.add((x, y))

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if is_valid((nx, ny), max_x, max_y) and grid[ny][nx] == crop and (nx, ny) not in visited:
                to_visit.append((nx, ny))

    return visited


def perimeter(points):
    deltas = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    return sum((p[0]+dx, p[1]+dy) not in points for p in points for dx, dy in deltas)


@profiler
def part_1():
    with open(input_file) as f:
        grid = [list(l.strip()) for l in f.readlines()]

    crops = []
    visited = set()
    for y, l in enumerate(grid):
        for x, h in enumerate(l):
            if (x, y) not in visited and h not in crops:
                v = flood_fill(grid, (x, y))
                crops.append(v)
                visited |= v

    print(sum(len(v) * perimeter(v) for v in crops))


def check_dir(points, p):
    px, py = p

    s1 = p in points and (px-1, py) not in points
    s2 = p in points and (px+1, py) not in points

    return s1, s2


def count_edges(points):

    xs = [p[0] for p in points]
    ys = [p[1] for p in points]

    edges = 0

    for x in range(min(xs), max(xs) + 1):
        s1 = False
        s2 = False
        for y in range(min(ys), max(ys) + 1):
            ns1, ns2 = check_dir(points, (x, y))
            edges += (int(ns1 and not s1) + (ns2 and not s2))
            s1, s2 = ns1, ns2

    return edges


@profiler
def part_2():
    with open(input_file) as f:
        grid = [list(l.strip()) for l in f.readlines()]

    crops = []
    visited = set()
    for y, l in enumerate(grid):
        for x, _ in enumerate(l):
            if (x, y) not in visited:
                v = flood_fill(grid, (x, y))
                crops.append(v)
                visited |= v

    print(sum(len(v) * 2 * count_edges(v) for v in crops))


if __name__ == "__main__":
    part_1()
    part_2()
