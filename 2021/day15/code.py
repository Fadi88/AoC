import time
import math
from collections import defaultdict
from queue import PriorityQueue as pq


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print(
            "Method "
            + method.__name__
            + " took : "
            + "{:2.5f}".format(time.time() - t)
            + " sec"
        )
        return ret

    return wrapper_method


@profiler
def part1():
    grid = []
    for l in open("day15/input.txt"):
        grid.append(list(map(int, l.strip())))

    deltas = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    visit = pq()
    visit.put((0, (0, 0)))

    risk = defaultdict(lambda: math.inf)
    risk[(0, 0)] = 0

    while not visit.empty():
        (r, (x, y)) = visit.get()

        for dx, dy in deltas:
            if 0 <= x + dx < len(grid) and 0 <= y + dy < len(grid[0]):
                new_risk = r + grid[x + dx][y + dy]
                if risk[(x + dx, y + dy)] > new_risk:
                    risk[(x + dx, y + dy)] = new_risk
                    visit.put((risk[(x + dx, y + dy)], (x + dx, y + dy)))

    print(risk[(len(grid) - 1, len(grid[0]) - 1)])


def get_risk(grid, x, y):
    tmp = grid[x % len(grid)][y % len(grid[0])] + x // len(grid) + y // len(grid[0])
    return (tmp - 1) % 9 + 1

@profiler
def part2():
    grid = []
    for l in open("day15/input.txt"):
        grid.append(list(map(int, l.strip())))

    deltas = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    visit = pq()
    visit.put((0, (0, 0)))

    risk = defaultdict(lambda: math.inf)
    risk[(0, 0)] = 0

    while not visit.empty():
        (r, (x, y)) = visit.get()

        for dx, dy in deltas:
            if 0 <= x + dx < 5 * len(grid) and 0 <= y + dy < 5 * len(grid[0]):
                new_risk = r + get_risk(grid, x + dx, y + dy)
                if risk[(x + dx, y + dy)] > new_risk:
                    risk[(x + dx, y + dy)] = new_risk
                    visit.put((risk[(x + dx, y + dy)], (x + dx, y + dy)))

    print(risk[(5 * len(grid) - 1, 5 * len(grid[0]) - 1)])


if __name__ == "__main__":

    part1()
    part2()
