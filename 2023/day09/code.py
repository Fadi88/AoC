# pylint: disable=C0114,C0116,C0301,C0209,W1514

from time import perf_counter


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print("Method " + method.__name__ + " took : " + "{:2.5f}".format(perf_counter() - t) + " sec")
        return ret

    return wrapper_method


def get_next(l):
    m = []
    m.append(l)
    while len(set(m[-1])) > 1:
        new_l = []
        for i in range(1, len(m[-1])):
            new_l.append(m[-1][i] - m[-1][i - 1])
        m.append(new_l)

    for i in reversed(range(len(m) - 1)):
        m[i].append(m[i + 1][-1] + m[i][-1])
    return m[0][-1]


@profiler
def part1():
    oasis = [list(map(int, l.split())) for l in open("day09/input.txt").read().splitlines()]

    print(sum([get_next(v) for v in oasis]))


@profiler
def part2():
    oasis = [list(map(int, l.split())) for l in open("day09/input.txt").read().splitlines()]

    print(sum([get_next(v[::-1]) for v in oasis]))


if __name__ == "__main__":
    part1()
    part2()
