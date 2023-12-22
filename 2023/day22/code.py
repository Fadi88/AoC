# pylint: disable=C0114,C0116,C0301,C0209,W1514,C0200

from time import perf_counter
from cProfile import run


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print("Method " + method.__name__ + " took : " + "{:2.5f}".format(perf_counter() - t) + " sec")
        return ret

    return wrapper_method


def drop(bricks, eraly=False):
    dropped = set()
    seen = set()

    for i in range(len(bricks)):
        pts = bricks[i]

        while True:
            new_pts = {(p[0], p[1], p[2] - 1) for p in pts}
            if all(p not in seen and p[2] > 0 for p in new_pts):
                bricks[i] = new_pts
                pts = new_pts
                dropped.add(i)
                if eraly:
                    return 1
            else:
                break

        seen.update(pts)

    return len(dropped)


@profiler
def part1():
    bricks = []

    for l in open("day22/input.txt"):
        p = list(map(lambda x: tuple(map(int, x.split(","))), l.strip().split("~")))
        b = set([p[0], p[1]])

        idx_deltas = [c1 != c2 for c1, c2 in zip(p[0], p[1])]
        if any(idx_deltas):
            assert sum(idx_deltas) == 1
            idx = idx_deltas.index(True)
            for val in range(min(p[0][idx], p[1][idx]), max(p[0][idx], p[1][idx])):
                b.add(tuple(val if i == idx else c for i, c in enumerate(p[0])))
        bricks.append(b)

    bricks.sort(key=lambda x: min(p[2] for p in x))

    drop(bricks)
    total = 0

    for i in range(len(bricks)):
        new_bricks = bricks.copy()
        del new_bricks[i]
        total += not drop(new_bricks, True)

    print(total)


@profiler
def part2():
    bricks = []

    for l in open("day22/input.txt"):
        p = list(map(lambda x: tuple(map(int, x.split(","))), l.strip().split("~")))
        b = set([p[0], p[1]])

        idx_deltas = [c1 != c2 for c1, c2 in zip(p[0], p[1])]
        if any(idx_deltas):
            assert sum(idx_deltas) == 1
            idx = idx_deltas.index(True)
            for val in range(min(p[0][idx], p[1][idx]), max(p[0][idx], p[1][idx])):
                b.add(tuple(val if i == idx else c for i, c in enumerate(p[0])))
        bricks.append(b)

    bricks.sort(key=lambda x: min(p[2] for p in x))

    drop(bricks)
    total = 0

    for i in range(len(bricks)):
        new_bricks = bricks.copy()
        del new_bricks[i]
        total += drop(new_bricks)

    print(total)


if __name__ == "__main__":
    part1()
    part2()
