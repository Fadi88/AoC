# pylint: disable=C0114, C0116, C0209

import time
import heapq

DEPTH = 10647
TARGET = (7, 770)

# DEPTH = 510
# TARGET = (10, 10)


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print("Method " + method.__name__ + " took : " + "{:2.5f}".format(time.time() - t) + " sec")
        return ret

    return wrapper_method


def get_cave():
    padding = 25
    cave_idx = [[-1] * (TARGET[0] + padding) for y in range(TARGET[1] + padding)]
    cave_ero = [[-1] * (TARGET[0] + padding) for y in range(TARGET[1] + padding)]
    cave_type = [[-1] * (TARGET[0] + padding) for y in range(TARGET[1] + padding)]

    for y in range(TARGET[1] + padding):
        for x in range(TARGET[0] + padding):
            if (x, y) == (0, 0) or (x, y) == TARGET:
                cave_idx[y][x] = 0
            elif y == 0:
                cave_idx[y][x] = x * 16807
            elif x == 0:
                cave_idx[y][x] = y * 48271
            else:
                cave_idx[y][x] = cave_ero[y][x - 1] * cave_ero[y - 1][x]
            cave_ero[y][x] = (cave_idx[y][x] + DEPTH) % 20183
            cave_type[y][x] = cave_ero[y][x] % 3

    return cave_type


@profiler
def part_1():
    cave_type = get_cave()
    print(sum([cave_type[y][x] for x in range(TARGET[0] + 1) for y in range(TARGET[1] + 1)]))


@profiler
def part_2():
    grid = get_cave()
    torch, ladder, neither = 0, 1, 2
    rocky, wet, narrow = 0, 1, 2

    allowed_tools = {
        rocky: [torch, ladder],
        wet: [ladder, neither],
        narrow: [torch, neither],
    }

    start = (torch, (0, 0), torch, torch)
    dst = (TARGET, torch)

    seen = set()
    to_visit = [start]

    deltas = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    while to_visit:
        d, p, t, pt = heapq.heappop(to_visit)

        if (p, t) in seen:
            continue

        if (p, t) == dst and pt == t:
            print(d)
            return

        seen.add((p, t))

        for dx, dy in deltas:
            nx, ny = p[0] + dx, p[1] + dy

            if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
                for nt in allowed_tools[grid[p[1]][p[0]]]:
                    if nt in allowed_tools[grid[ny][nx]]:
                        step = 1 if nt == t else 8
                        heapq.heappush(to_visit, (d + step, (nx, ny), nt, t))


if __name__ == "__main__":
    part_1()
    part_2()
