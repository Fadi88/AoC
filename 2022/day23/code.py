from time import time as perf_counter
from collections import defaultdict, deque


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print('Method ' + method.__name__ + ' took : ' +
              "{:2.5f}".format(perf_counter()-t) + ' sec')
        return ret
    return wrapper_method


@profiler
def part1():
    grid = set()
    for y, l in enumerate(open("day23/test.txt").read().splitlines()):
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
        proposal = defaultdict(list)

        for e in grid:
            if sum((e[0] + dx , e[1] + dy) in grid for dx in [-1,1,0] for dy in [-1,1,0]) == 1:
                continue

            for d in directions:
                if all((e[0]+delta[0], e[1]+delta[1]) not in grid for delta in neighbors[d]):
                    proposal[e].append(
                        (e[0]+neighbors[d][0][0], e[1]+neighbors[d][0][1]))
                    break
        new_grid = set()
        for e in grid:
            if len(proposal[e]) == 0:
                new_grid.add(e)
            else:
                moved = False
                for p in proposal[e]:
                    if not any(p in proposal[e2] for e2 in proposal if e2 != e):
                        new_grid.add(p)
                        moved = True
                        break

                if not moved:
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
    for y, l in enumerate(open("day23/input.txt").read().splitlines()):
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
        proposal = defaultdict(list)

        for e in grid:
            if sum((e[0] + dx , e[1] + dy) in grid for dx in [-1,1,0] for dy in [-1,1,0]) == 1:
                continue
    
            for d in directions:
                if all((e[0]+delta[0], e[1]+delta[1]) not in grid for delta in neighbors[d]):
                    proposal[e].append(
                        (e[0]+neighbors[d][0][0], e[1]+neighbors[d][0][1]))
                    break
        new_grid = set()
        for e in grid:
            if len(proposal[e]) == 0:
                new_grid.add(e)
            else:
                moved = False
                for p in proposal[e]:
                    if not any(p in proposal[e2] for e2 in proposal if e2 != e):
                        new_grid.add(p)
                        moved = True
                        break

                if not moved:
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
