import time
import re
from collections import defaultdict


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print('Method ' + method.__name__ + ' took : ' +
              "{:2.5f}".format(time.time()-t) + ' sec')
        return ret
    return wrapper_method


def print_grid(g, s):
    for y in range(s):
        for x in range(s):
            if (x, y) in g:
                print('#', end='')
            else:
                print('.', end='')
        print()
    print()


@profiler
def part1():

    lights = set()
    with open('input.txt') as f:
        y = 0
        for l in f:
            for x in range(len(l)):
                if l[x] == '#':
                    lights.add((x, y))
            y += 1

    dirs = [(0, 1), (0, -1), (1, 1), (1, -1),
            (1, 0), (-1, 1), (-1, -1), (-1, 0)]

    for _ in range(100):
        reach = defaultdict(int)

        for x, y in lights:
            for dx, dy in dirs:
                if x+dx < 0 or x+dx > 99 or y+dy < 0 or y+dy > 99:
                    continue
                reach[(x+dx, y+dy)] += 1

        new_lights = set()

        for p in lights:
            if reach[p] == 2 or reach[p] == 3:
                new_lights.add(p)

        for p in reach:
            if p not in lights and reach[p] == 3:
                new_lights.add(p)

        lights = new_lights

    print(len(lights))


@profiler
def part2():

    size = 100
    lights = set()

    with open('input.txt') as f:
        y = 0
        for l in f:
            for x in range(len(l)):
                if l[x] == '#':
                    lights.add((x, y))
            y += 1

    dirs = [(0, 1), (0, -1), (1, 1), (1, -1),
            (1, 0), (-1, 1), (-1, -1), (-1, 0)]

    always_on = [(0, 0), (size-1, 0), (0, size-1), (size-1, size-1)]

    for p in always_on:
        lights.add(p)

    for _ in range(100):
        reach = defaultdict(int)

        for p in always_on:
            lights.add(p)

        for x, y in lights:
            for dx, dy in dirs:
                if x+dx < 0 or x+dx > size-1 or y+dy < 0 or y+dy > size-1:
                    continue
                reach[(x+dx, y+dy)] += 1

        new_lights = set()

        for p in lights:
            if reach[p] == 2 or reach[p] == 3:
                new_lights.add(p)

        for p in reach:
            if p not in lights and reach[p] == 3:
                new_lights.add(p)

        lights = new_lights
        for p in always_on:
            lights.add(p)

    print(len(lights))


if __name__ == "__main__":

    part1()
    part2()
