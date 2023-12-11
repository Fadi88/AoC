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


def augment_by_n(galaxies, empty_x, empty_y, n):
    new_galaxies = set()
    for g in galaxies:
        n_x = g.real + (n - 1) * sum(list(map(lambda x: x < g.real, empty_x)))
        n_y = g.imag + (n - 1) * sum(list(map(lambda x: x < g.imag, empty_y)))

        new_galaxies.add(n_x + n_y * 1j)
    return new_galaxies


def get_empty_x(data):
    empty_x = []
    for x in range(len(data[0])):
        if [l[x] for l in data].count("#") == 0:
            empty_x.append(x)

    return empty_x


def get_empty_y(data):
    empty_y = []
    for y, l in enumerate(data):
        if l.count("#") == 0:
            empty_y.append(y)
    return empty_y


def get_galaxies(data):
    galaxies = set()
    for y, l in enumerate(data):
        for x, c in enumerate(l):
            if c == "#":
                galaxies.add(x + y * 1j)

    return galaxies


def get_dist(pair):
    p1 = pair[0]
    p2 = pair[1]
    return int(abs(p1.real - p2.real) + abs(p1.imag - p2.imag))


@profiler
def part1():
    data = open("day11/input.txt").read().splitlines()

    galaxies = get_galaxies(data)

    empty_y = get_empty_y(data)
    empty_x = get_empty_x(data)

    new_galaxies = augment_by_n(galaxies, empty_x, empty_y, 2)

    print(sum(map(get_dist,combinations(new_galaxies, 2))))


@profiler
def part2():
    data = open("day11/input.txt").read().splitlines()

    galaxies = get_galaxies(data)

    empty_y = get_empty_y(data)
    empty_x = get_empty_x(data)

    new_galaxies = augment_by_n(galaxies, empty_x, empty_y, 1000000)

    print(sum(map(get_dist,combinations(new_galaxies, 2))))


if __name__ == "__main__":
    part1()
    part2()
