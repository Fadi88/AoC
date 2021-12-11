import time
from collections import deque


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print('Method ' + method.__name__ + ' took : ' +
              "{:2.5f}".format(time.time()-t) + ' sec')
        return ret
    return wrapper_method


def get_deltas():
    return [(0, 1), (0, -1), (1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1)]


def print_grid(grid):
    for l in grid:
        print(' '.join(map(str, l)))
    print()


def cycle(grid):
    flashes = 0

    visited = set()
    ready = deque()

    for x in range(len(grid)):
        for y in range(len(grid[0])):
            grid[x][y] += 1
            if grid[x][y] > 9:
                ready.append((x, y))
                visited.add((x, y))

    while ready:
        nx, ny = ready.popleft()
        for dx, dy in get_deltas():
            if 0 <= nx+dx < len(grid) and 0 <= ny+dy < len(grid[0]):
                grid[nx+dx][ny+dy] += 1
                if grid[nx+dx][ny+dy] > 9 and (nx+dx, ny+dy) not in visited:
                    ready.append((nx+dx, ny+dy))
                    visited.add((nx+dx, ny+dy))

    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] > 9:
                grid[x][y] = 0
                flashes += 1

    return flashes


@profiler
def part1():
    grid = [list(map(int, list(l.strip()))) for l in open("day11/input.txt")]

    flashes = 0

    for _ in range(100):
        flashes += cycle(grid)

    print(flashes)


@profiler
def part2():

    grid = [list(map(int, list(l.strip()))) for l in open("day11/input.txt")]

    ready = deque()

    cnt = 0
    while True:
        if all([all([i == 0 for i in l]) for l in grid]):
            break
        cnt += 1
        cycle(grid)

    print(cnt)


if __name__ == "__main__":

    part1()
    part2()
