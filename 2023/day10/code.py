# pylint: disable=C0114,C0116,C0301,C0209,W1514

from time import perf_counter
from matplotlib.path import Path


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print("Method " + method.__name__ + " took : " + "{:2.5f}".format(perf_counter() - t) + " sec")
        return ret

    return wrapper_method


@profiler
def part1():
    maze = {}
    ground = []
    directions = {"|": [+1j, -1j], "-": [+1, -1], "L": [+1, -1j], "J": [-1, -1j], "7": [-1, 1j], "F": [1, 1j]}
    for y, l in enumerate(open("day10/input.txt").read().splitlines()):
        for x, c in enumerate(l):
            if c in directions:
                cp = x + y * 1j
                maze[cp] = [cp + directions[c][0], cp + directions[c][1]]
            elif c == "S":
                start = x + y * 1j
            elif c == ".":
                ground.append(x + y * 1j)

    maze[start] = [l for l in maze for n in maze[l] if n == start]

    to_visit = [start]

    dst = {start: 0}

    while to_visit:
        cp = to_visit.pop(0)

        for np in maze[cp]:
            if np in maze and np not in dst:
                dst[np] = dst[cp] + 1
                to_visit.append(np)

    print(max(dst.values()))


@profiler
def part2():
    maze = {}
    directions = {"|": [+1j, -1j], "-": [+1, -1], "L": [+1, -1j], "J": [-1, -1j], "7": [-1, 1j], "F": [1, 1j]}

    for y, l in enumerate(open("day10/input.txt").read().splitlines()):
        ymax = y
        for x, c in enumerate(l):
            xmax = x
            if c in directions:
                cp = x + y * 1j
                maze[cp] = [cp + directions[c][0], cp + directions[c][1]]
            elif c == "S":
                start = x + y * 1j

    maze[start] = [l for l in maze for n in maze[l] if n == start]

    to_visit = [start]

    dst = {start: 0}

    while to_visit:
        cp = to_visit.pop(0)

        for np in maze[cp]:
            if np in maze and np not in dst:
                dst[np] = dst[cp] + 1
                to_visit.append(np)
                break

    polygone = Path([(p.real, p.imag) for p in dst.keys()])

    total = 0
    for y in range(ymax):
        for x in range(xmax):
            if x + y*1j not in dst and polygone.contains_point((x,y)):
                total += 1
    print(total)


if __name__ == "__main__":
    part1()
    part2()
