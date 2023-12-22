# pylint: disable=C0114,C0116,C0301,C0209,W1514

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
    grid = set()

    for y, l in enumerate(open("day21/input.txt")):
        for x, c in enumerate(l):
            if c == "#":
                grid.add(x + y * 1j)
            elif c == "S":
                start = x + y * 1j

    deltas = [1, -1, -1j, 1j]

    reach = {0: set([start])}

    while len(reach) <= 64:
        steps = max(reach.keys())

        reach[steps + 1] = set()

        for pos in reach[steps]:
            for d in deltas:
                if pos + d not in grid:
                    reach[steps + 1].add(pos + d)

    print(len(reach[64]))


@profiler
def part2():
    grid = set()
    free = set()

    x = 0
    for y, l in enumerate(open("day21/input.txt")):
        for x, c in enumerate(l):
            if c == "#":
                grid.add(x + y * 1j)
            elif c == "S":
                start = x + y * 1j
            elif c == ".":
                free.add(x + y * 1j)

    deltas = [1, -1, -1j, 1j]

    reach = {0: set([start])}

    grid_len = x + 1
    pts = []
    target_time = 26501365
    while len(pts) < 3:
        steps = max(reach.keys())

        if steps - 1 in reach:
            del reach[steps - 1]

        reach[steps + 1] = set()

        for pos in reach[steps]:
            for d in deltas:
                npt = pos + d
                nx = npt.real % grid_len
                ny = npt.imag % grid_len
                if nx + ny * 1j not in grid:
                    reach[steps + 1].add(pos + d)
        if (steps - (grid_len // 2) + 1) % grid_len == 0:
            pts.append(len(reach[max(reach.keys())]))

    c = pts[0]
    b = pts[1] - pts[0]
    a = pts[2] - pts[1]

    x = target_time // grid_len # remainder is already in the euqtion
    assert grid_len // 2 == target_time%grid_len

    print(c + b * x + (x * (x - 1) // 2) * (a - b))


if __name__ == "__main__":
    part1()
    part2()
