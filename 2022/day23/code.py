from time import time as perf_counter
from collections import Counter, defaultdict, deque


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print('Method ' + method.__name__ + ' took : ' +
              "{:2.5f}".format(perf_counter()-t) + ' sec')
        return ret
    return wrapper_method


def is_isolated(grid, e):
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == dy == 0:
                continue
            if (e[0] + dx, e[1] + dy) in grid:
                return False

    return True


@profiler
def part1():
    grid = set()
    for y, l in enumerate(open("input.txt").read().splitlines()):
        for x, c in enumerate(l):
            if c == "#":
                grid.add((x, y))

    directions = deque(["north", "south", "west", "east"])

    neighbors = {
        "north": [(0, -1), (1, -1), (-1, -1)],
        "south": [(0, 1), (1, 1), (-1, 1)],
        "west": [(-1, 0), (-1, 1), (-1, -1)],
        "east": [(1, 0), (1, 1), (1, -1)],
    }

    for _ in range(10):
        proposal = {}
        counts = Counter()

        for e in grid:
            if is_isolated(grid, e):
                continue
        
            for d in directions:
                if all((e[0]+delta[0], e[1]+delta[1]) not in grid for delta in neighbors[d]):
                    proposal[e] = (e[0]+neighbors[d][0][0],
                                   e[1]+neighbors[d][0][1])
                    counts[(e[0]+neighbors[d][0][0],
                            e[1]+neighbors[d][0][1])] += 1
                    break

        new_grid = set()
        for e in grid:
            if e in proposal and counts[proposal[e]] == 1:
                new_grid.add(proposal[e])
            else:
                new_grid.add(e)

        assert(len(grid) == len(new_grid))
        grid = new_grid
        directions.rotate(-1)

    xs = set(e[0] for e in grid)
    ys = set(e[1] for e in grid)
    print((max(xs) - min(xs) + 1) * (max(ys) - min(ys)+1) - len(grid))


@profiler
def part2():
    grid = set()
    for y, l in enumerate(open("input.txt").read().splitlines()):
        for x, c in enumerate(l):
            if c == "#":
                grid.add((x, y))

    directions = deque(["north", "south", "west", "east"])

    neighbors = {
        "north": [(0, -1), (1, -1), (-1, -1)],
        "south": [(0, 1), (1, 1), (-1, 1)],
        "west": [(-1, 0), (-1, 1), (-1, -1)],
        "east": [(1, 0), (1, 1), (1, -1)],
    }

    cycle = 0

    while True:
        proposal = {}
        counts = Counter()

        for e in grid:
            if is_isolated(grid, e):
                continue
        
            for d in directions:
                if all((e[0]+delta[0], e[1]+delta[1]) not in grid for delta in neighbors[d]):
                    proposal[e] = (e[0]+neighbors[d][0][0],
                                   e[1]+neighbors[d][0][1])
                    counts[(e[0]+neighbors[d][0][0],
                            e[1]+neighbors[d][0][1])] += 1
                    break

        new_grid = set()
        for e in grid:
            if e in proposal and counts[proposal[e]] == 1:
                new_grid.add(proposal[e])
            else:
                new_grid.add(e)

        assert(len(grid) == len(new_grid))
        cycle += 1
        if grid == new_grid:
            break
        grid = new_grid
        directions.rotate(-1)

    print(cycle)


if __name__ == "__main__":

    part1()
    part2()

import cProfile

#cProfile.run("part2()")
