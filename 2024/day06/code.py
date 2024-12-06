# pylint: disable=C0114,C0116,C0301,C0209,W1514

from time import time as perf_counter


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print("Method " + method.__name__ + " took : " + "{:2.5f}".format(perf_counter() - t) + " sec")
        return ret

    return wrapper_method


@profiler
def part1():
    obstacles = set()
    dirs = {"^": (0, -1), ">": (1, 0), "v": (0, 1), "<": (-1, 0)}

    rot = "^>v<"

    for y, l in enumerate(open("day06/input.txt").read().splitlines()):
        for x, c in enumerate(l):
            if c == "#":
                obstacles.add((x, y))
            elif c in dirs:
                guard = (c, (x, y))

    seen = set()
    while guard not in seen:
        seen.add(guard)

        np = (guard[1][0] + dirs[guard[0]][0], guard[1][1] + dirs[guard[0]][1])
        d = guard[0]
        if np in obstacles:
            d = rot[(rot.index(d) + 1) % len(rot)]
            np = (guard[1][0] + dirs[d][0], guard[1][1] + dirs[d][1])

        if not (0 <= np[0] < len(l) and 0 <= np[1] < y):
            break
        guard = (d, np)

    path = set(guard[1] for guard in seen)
    print(len(path))

    return path


def loop(guard, obstacles, max_x, max_y):
    dirs = {"^": (0, -1), ">": (1, 0), "v": (0, 1), "<": (-1, 0)}
    rot = "^>v<"

    seen = set()
    while guard not in seen:
        seen.add(guard)

        np = (guard[1][0] + dirs[guard[0]][0], guard[1][1] + dirs[guard[0]][1])
        d = guard[0]
        if np in obstacles:
            for _ in range(len(rot)):
                d = rot[(rot.index(d) + 1) % len(rot)]
                np = (guard[1][0] + dirs[d][0], guard[1][1] + dirs[d][1])
                if np not in obstacles:
                    break

        if not (0 <= np[0] < max_x and 0 <= np[1] < max_y):
            return False  # no loop out of grid

        guard = (d, np)

    return True  # loop


@profiler
def part2(path):
    obstacles = set()

    for y, l in enumerate(open("day06/input.txt").read().splitlines()):
        for x, c in enumerate(l):
            if c == "#":
                obstacles.add((x, y))
            elif c == "^":
                guard = (c, (x, y))

    print(sum(loop(guard, obstacles | {t}, len(l), y) for t in path))


if __name__ == "__main__":
    path = part1()
    part2(path)
