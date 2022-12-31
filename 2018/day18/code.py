import time
from collections import Counter


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print("Method " + method.__name__ + " took : " +
              "{:2.5f}".format(time.time() - t) + " sec")
        return ret

    return wrapper_method


@profiler
def part_1():
    grid = {}

    for y, l in enumerate(open("day18/input.txt").read().splitlines()):
        for x, c in enumerate(l):
            if c in ["#", "|"]:
                grid[(x, y)] = c

    for _ in range(10):
        tree_counter = Counter()
        lumberyard_counter = Counter()

        for pos in grid:
            if grid[pos] == "|":
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == dy == 0:
                            continue
                        nx = pos[0] + dx
                        ny = pos[1] + dy

                        if not (0 <= nx < 50 and 0 <= ny < 50):
                            continue

                        if (nx, ny) not in grid or grid[(nx, ny)] == "#":
                            tree_counter[(nx, ny)] += 1
            elif grid[pos] == "#":
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == dy == 0:
                            continue
                        nx = pos[0] + dx
                        ny = pos[1] + dy
                        if not (0 <= nx < 50 and 0 <= ny < 50):
                            continue

                        if (nx, ny) in grid:
                            lumberyard_counter[(nx, ny)] += 1

        new_grid = {}

        for t in tree_counter:
            if t not in grid and tree_counter[t] >= 3:
                new_grid[t] = "|"
        for p in grid:
            if grid[p] == "|":
                if p in lumberyard_counter and lumberyard_counter[p] >= 3:
                    new_grid[p] = "#"
                else:
                    new_grid[p] = "|"
            elif grid[p] == "#" and p in lumberyard_counter and lumberyard_counter[p] > 0 and p in tree_counter and tree_counter[p] > 0:
                new_grid[p] = "#"

        grid = new_grid

    print(list(grid.values()).count("#") * list(grid.values()).count("|"))


def get_hash(grid):
    ret = ""
    xs = [p[0] for p in grid]
    ys = [p[1] for p in grid]
    for y in range(min(ys), max(ys) + 1):
        for x in range(min(xs), max(xs) + 1):
            if (x, y) in grid:
                ret += grid[(x, y)]
            else:
                ret += "."

        ret += "\n"

    return ret


@profiler
def part_2():
    grid = {}

    for y, l in enumerate(open("day18/input.txt").read().splitlines()):
        for x, c in enumerate(l):
            if c in ["#", "|"]:
                grid[(x, y)] = c

    seen = []
    score = {}

    for i in range(1000000000):
        tree_counter = Counter()
        lumberyard_counter = Counter()

        grid_hash = get_hash(grid)

        if grid_hash in seen:
            cycle_begin = seen.index(grid_hash)
            period = i - cycle_begin
            break

        seen.append(grid_hash)

        for pos in grid:
            if grid[pos] == "|":
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == dy == 0:
                            continue
                        nx = pos[0] + dx
                        ny = pos[1] + dy

                        if not (0 <= nx < 50 and 0 <= ny < 50):
                            continue

                        if (nx, ny) not in grid or grid[(nx, ny)] == "#":
                            tree_counter[(nx, ny)] += 1
            elif grid[pos] == "#":
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == dy == 0:
                            continue
                        nx = pos[0] + dx
                        ny = pos[1] + dy
                        if not (0 <= nx < 50 and 0 <= ny < 50):
                            continue

                        if (nx, ny) in grid:
                            lumberyard_counter[(nx, ny)] += 1

        new_grid = {}

        for t in tree_counter:
            if t not in grid and tree_counter[t] >= 3:
                new_grid[t] = "|"
        for p in grid:
            if grid[p] == "|":
                if p in lumberyard_counter and lumberyard_counter[p] >= 3:
                    new_grid[p] = "#"
                else:
                    new_grid[p] = "|"
            elif grid[p] == "#" and p in lumberyard_counter and lumberyard_counter[p] > 0 and p in tree_counter and tree_counter[p] > 0:
                new_grid[p] = "#"

        grid = new_grid

        score[i] = list(grid.values()).count("#") * \
            list(grid.values()).count("|")

    print(score[cycle_begin + ((1000000000 - cycle_begin) % period) - 1])


if __name__ == "__main__":

    part_1()
    part_2()
