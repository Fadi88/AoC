import time
import re
from collections import deque


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
    for i in grid:
        for o in grid:
            if o == i:
                continue
            a = grid[i]
            b = grid[o]

            if a[1] <= b[0] - b[1] and a[1] > 0:
                cnt += 1

    print(cnt)


@profiler
def part2():
    nodes = {}
    with open('input.txt') as f:
        lines = f.read().splitlines()[2:]

    for line in lines:
        parts = line.split()
        coords = re.findall(r'-x(\d+)-y(\d+)', line)
        x, y = int(coords[0][0]), int(coords[0][1])
        nodes[(x, y)] = [int(parts[1][:-1]), int(parts[2][:-1])]

    max_x = max(x for x, _ in nodes)
    max_y = max(y for _, y in nodes)

    empty_node = None
    node_grid = [['#' if nodes[(x, y)][0] > 100 else '.' for x in range(
        max_x + 1)] for y in range(max_y + 1)]

    for (x, y), node in nodes.items():
        if node[1] == 0:
            empty_node = (x, y)
            break

    if empty_node is None:
        raise ValueError("No empty node found")

    queue = [(empty_node, (max_x, 0), 0)]
    visited = set()
    visited.add((empty_node, (max_x, 0)))

    while queue:
        empty, goal, steps = queue.pop(0)

        if goal == (0, 0):
            print(steps)
            break

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_empty = (empty[0] + dx, empty[1] + dy)
            if 0 <= new_empty[0] <= max_x and 0 <= new_empty[1] <= max_y and node_grid[new_empty[1]][new_empty[0]] != '#':
                new_goal = goal if new_empty != goal else empty

                if (new_empty, new_goal) not in visited:
                    visited.add((new_empty, new_goal))
                    queue.append((new_empty, new_goal, steps + 1))


if __name__ == "__main__":

    part1()
    part2()
