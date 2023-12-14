# pylint: disable=C0114,C0116,C0301,C0209,W1514,C0200

from time import perf_counter

def profiler(method):
    def wrapper_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print("Method " + method.__name__ + " took : " + "{:2.5f}".format(perf_counter() - t) + " sec")
        return ret

    return wrapper_method


@profiler
def part1():
    round_rocks = set()
    cube_rocks = set()

    for y, l in enumerate(open("day14/input.txt")):
        max_y = y
        for x, c in enumerate(l):
            match c:
                case "O":
                    round_rocks.add(x + y * 1j)
                case "#":
                    cube_rocks.add(x + y * 1j)

    tilted = set()
    for x in set([int(o.real) for o in round_rocks]):
        ys_o = [int(o.imag) for o in round_rocks if int(o.real) == x]
        ys_c = [int(o.imag) for o in cube_rocks if int(o.real) == x]

        ys_o.sort()
        ys_c.sort()

        for y in ys_o:
            upper_cube = -1
            for c in cube_rocks:
                if int(c.imag) < y and int(c.real) == x:
                    upper_cube = max(int(c.imag), upper_cube)

            n_y = max([upper_cube] + [int(c.imag) for c in tilted if int(c.real) == x and int(c.imag) < y]) + 1

            tilted.add(x + n_y * 1j)

    total = 0
    for r in tilted:
        total += max_y - int(r.imag) + 1
    print(total)


def shift_up(grid):
    for x in range(len(grid[0])):
        last_free = -1
        for y in range(len(grid)):
            match grid[y][x]:
                case ".":
                    if last_free == -1:
                        last_free = y
                case "#":
                    last_free = -1
                case "O":
                    if last_free != -1:
                        grid[y][x] = "."
                        grid[last_free][x] = "O"
                        last_free += 1


def rotate_cw(grid):
    return list(map(list, zip(*grid[::-1])))


def full_rotation_cw(grid):
    for _ in range(4):
        shift_up(grid)
        grid = rotate_cw(grid)
    return grid


def get_score(grid):
    total = 0

    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == "O":
                total += len(grid) - y

    return total


@profiler
def part2():
    grid = []

    for l in open("day14/input.txt"):
        grid.append(list(l.strip()))

    cache = {}
    seen = {}
    n = 1000000000
    for t in range(1, n):
        grid = full_rotation_cw(grid)
        if str(grid) in seen:
            cycle_begin = seen[str(grid)]
            cycle_length = t - cycle_begin
            break
        cache[t] = get_score(grid)
        seen[str(grid)] = t

    grid_n = ((n - cycle_begin) % cycle_length) + cycle_begin
    print(cache[grid_n])

if __name__ == "__main__":
    part1()
    part2()
