# pylint: disable=C0114,C0116,C0301,C0209,W1514

from time import perf_counter
from itertools import combinations


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print("Method " + method.__name__ + " took : " + "{:2.5f}".format(perf_counter() - t) + " sec")
        return ret

    return wrapper_method


@profiler
def part1():
    galaxies = set()

    data = open("day11/input.txt").read().splitlines()
    augemented_x = [[] for _ in range(len(data))]

    for x in range(len(data[0])):
        if [l[x] for l in data].count("#") == 0:
            for y in range(len(data)):
                augemented_x[y] += [".", "."]
        else:
            for y in range(len(data)):
                augemented_x[y].append(data[y][x])

    augemented_y = []
    for l in augemented_x:
        augemented_y.append(l)
        if l.count("#") == 0:
            augemented_y.append(l)

    for y, l in enumerate(augemented_y):
        for x, c in enumerate(l):
            if c == "#":
                galaxies.add(x + y * 1j)

    dist = []
    for p1, p2 in combinations(galaxies, 2):
        dist.append(int(abs(p1.real - p2.real) + abs(p1.imag - p2.imag)))

    print(sum(dist))


@profiler
def part2():
    galaxies = set()

    data = open("day11/input.txt").read().splitlines()

    for y, l in enumerate(data):
        for x, c in enumerate(l):
            if c == "#":
                galaxies.add(x + y * 1j)

    empty_y = []
    for y, l in enumerate(data):
        if l.count("#") == 0:
            empty_y.append(y)

    empty_x = []
    for x in range(len(data[0])):
        if [l[x] for l in data].count("#") == 0:
            empty_x.append(x)

    new_galaxies = set()
    for g in galaxies:
        n_x = g.real + (1000000 - 1) * sum(list(map(lambda x: x < g.real, empty_x)))
        n_y = g.imag + (1000000 - 1) * sum(list(map(lambda x: x < g.imag, empty_y)))

        new_galaxies.add(n_x + n_y * 1j)

    dist = []
    for p1, p2 in combinations(new_galaxies, 2):
        dist.append(int(abs(p1.real - p2.real) + abs(p1.imag - p2.imag)))

    print(sum(dist))


if __name__ == "__main__":
    part1()
    part2()
