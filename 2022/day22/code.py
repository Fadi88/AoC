from time import perf_counter
import re
from collections import Counter


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

    p = open("day22/input.txt").read().split("\n\n")

    grid = {}
    direction = 0
    moves = {
        0: (1, 0),
        1: (0, 1),
        2: (-1, 0),
        3: (0, -1),
    }

    for y, l in enumerate(p[0].splitlines()):
        for x, c in enumerate(l):
            if c in [".", "#"]:
                if len(grid) == 0:
                    pos = (x, y)
                grid[(x, y)] = c

    path = re.findall(r"\w?\d+", p[1])

    for s in path:
        if "R" in s:
            direction = (direction + 1) % 4
            s = s.replace("R", "")
        elif "L" in s:
            direction = (direction - 1) % 4
            s = s.replace("L", "")

        for _ in range(int(s)):
            if (pos[0] + moves[direction][0], pos[1] + moves[direction][1]) in grid:
                if grid[(pos[0] + moves[direction][0], pos[1] + moves[direction][1])] == ".":
                    pos = (pos[0] + moves[direction][0],
                           pos[1] + moves[direction][1])
                else:
                    break
            else:
                if direction in [0, 2]:
                    x = {
                        0: min([tile[0] for tile in grid if tile[1] == pos[1]]),
                        2: max([tile[0] for tile in grid if tile[1] == pos[1]]),
                    }
                    n_pos = (x[direction], pos[1])
                else:
                    y = {
                        1: min([tile[1] for tile in grid if tile[0] == pos[0]]),
                        3: max([tile[1] for tile in grid if tile[0] == pos[0]]),
                    }
                    n_pos = (pos[0], y[direction])

                if grid[n_pos] == ".":
                    pos = n_pos
                else:
                    break

            assert(pos in grid and grid[pos] == ".")

    print(1000*(pos[1]+1) + 4 * (pos[0]+1) + direction)


def get_face(p):

    #          /-----X-----\
    #          |  1  |  2  |
    #          X-----X-----/
    #          |  3  |
    #    /-----X-----X
    #    |  5  |  4  |
    #    X-----x-----/
    #    |  6  |
    #    \-----/

    x, y = p
    if y // 50 == 0:
        return x // 50
    elif y // 50 == 1:
        return 3
    elif y // 50 == 2:
        return {0: 5, 1: 4}[x // 50]
    else:
        return 6


@profiler
def part2():
    p = open("day22/input.txt").read().split("\n\n")

    grid = {}
    direction = 0
    moves = {
        0: (1, 0),
        1: (0, 1),
        2: (-1, 0),
        3: (0, -1),
    }
    # from (face number, direction) to (new direction, conversion between coordinates lambda)
    # Facing is 0 for right (>), 1 for down (v), 2 for left (<), and 3 for up (^)
    wrap = {
        (1, 2): (0, lambda x, y: (0, 149 - y)),
        (1, 3): (0, lambda x, y: (0, x+100)),
        (2, 0): (2, lambda x, y: (99, 149-y)),
        (2, 1): (2, lambda x, y: (99, x-50)),
        (2, 3): (3, lambda x, y: (x-100, 199)),
        (3, 0): (3, lambda x, y: (y+50, 49)),
        (3, 2): (1, lambda x, y: (y-50, 100)),
        (4, 0): (2, lambda x, y: (149, 149-y)),
        (4, 1): (2, lambda x, y: (49, 100+x)),
        (5, 2): (0, lambda x, y: (50, 149-y)),
        (5, 3): (0, lambda x, y: (50, 50+x)),
        (6, 0): (3, lambda x, y: (y-100, 149)),
        (6, 1): (1, lambda x, y: (x+100, 0)),
        (6, 2): (1, lambda x, y: (y-100, 0)),
    }
    for y, l in enumerate(p[0].splitlines()):
        for x, c in enumerate(l):
            if c in [".", "#"]:
                if len(grid) == 0:
                    pos = (x, y)
                grid[(x, y)] = c

    path = re.findall(r"\w?\d+", p[1])

    for s in path:
        if "R" in s:
            direction = (direction + 1) % 4
            s = s.replace("R", "")
        elif "L" in s:
            direction = (direction - 1) % 4
            s = s.replace("L", "")

        for _ in range(int(s)):
            if (pos[0] + moves[direction][0], pos[1] + moves[direction][1]) in grid:
                if grid[(pos[0] + moves[direction][0], pos[1] + moves[direction][1])] == ".":
                    pos = (pos[0] + moves[direction][0],
                           pos[1] + moves[direction][1])
                else:
                    break
            else:
                n_d, fn = wrap[(get_face(pos), direction)]
                n_pos = fn(pos[0], pos[1])
                assert(n_pos in grid)
                if n_pos not in grid:
                    pass
                if grid[n_pos] == ".":
                    direction = n_d
                    pos = n_pos
                else:
                    break

    print(1000*(pos[1]+1) + 4 * (pos[0]+1) + direction)

if __name__ == "__main__":

    part1()
    part2()
