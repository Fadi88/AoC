import time
import re
from itertools import combinations


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print('Method ' + method.__name__ + ' took : ' +
              "{:2.5f}".format(time.time()-t) + ' sec')
        return ret
    return wrapper_method


@profiler
def part1():

    grid = {}
    for l in open('input.txt').read().split('\n')[2:]:
        p = l.split()

        g = re.findall(r'-x(\d+)-y(\d+)', l)
        grid[(int(g[0][0]), int(g[0][1]))] = [int(p[1][:-1]), int(p[2][:-1])]

    cnt = 0
    for a, b in combinations(grid.values(), 2):
        cnt += int(a[1] <= b[0] - b[1] and a[1] != 0) + \
            int(b[1] <= a[0] - a[1] and b[1] != 0)
    print(cnt)


@profiler
def part2():
    max_x, max_y = 0, 0
    node_grid = {}
    empty_node = None

    with open('input.txt') as f:
        lines = f.read().splitlines()[2:]

    for line in lines:
        parts = line.split()
        coords = re.findall(r'-x(\d+)-y(\d+)', line)
        x, y = map(int, coords[0])
        size, used = map(int, (parts[1][:-1], parts[2][:-1]))
        max_x, max_y = max(max_x, x), max(max_y, y)
        if used == 0:
            empty_node = (x, y)
        node_grid[(x, y)] = '#' if size > 100 else '.'

    queue = [(empty_node, (max_x, 0), 0)]
    visited = set()
    visited.add((empty_node, (max_x, 0)))

    while queue:
        empty, goal, steps = queue.pop(0)

        if goal == (0, 0):
            print(steps)
            break

        for dx, dy in [(0, -1), (0, 1), (1, 0), (-1, 0)]:
            new_empty = (empty[0] + dx, empty[1] + dy)
            new_goal = goal
            if (0 <= new_empty[0] <= max_x and
                0 <= new_empty[1] <= max_y and
                    node_grid.get(new_empty, '#') != '#'):
                if new_empty == goal:
                    # sawp empty and goal, move data to empty and mark its spot as free
                    new_goal = empty
                    new_empty = goal

                if (new_empty, new_goal) not in visited:
                    visited.add((new_empty, new_goal))
                    queue.append((new_empty, new_goal, steps + 1))


if __name__ == "__main__":

    part1()
    part2()
