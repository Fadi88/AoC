# pylint: disable=C0114,C0116,C0301,C0209,W1514

from time import perf_counter


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print("Method " + method.__name__ + " took : " + "{:2.5f}".format(perf_counter() - t) + " sec")
        return ret

    return wrapper_method


def shoe_lace(points):
    res = sum(points[i - 1][0] * points[i][1] - points[i - 1][1] * points[i][0] for i in range(len(points)))
    return res // 2


@profiler
def part1():
    polygon = [(0, 0)]

    deltas = {"R": (1, 0), "L": (-1, 0), "U": (0, -1), "D": (0, 1)}

    p_cnt = 0

    for l in open("day18/input.txt"):
        ps = l.split()
        d = deltas[ps[0]]
        lp = polygon[-1]
        steps = int(ps[1])
        p_cnt += steps
        polygon.append((lp[0] + d[0] * steps, lp[1] + d[1] * steps))

    print(shoe_lace(polygon) + p_cnt // 2 + 1)


@profiler
def part2():
    polygon = [(0, 0)]

    deltas = {"R": (1, 0), "L": (-1, 0), "U": (0, -1), "D": (0, 1)}

    hex2d = {
        "0": "R",
        "1": "D",
        "2": "L",
        "3": "U",
    }

    p_cnt = 0

    for l in open("day18/input.txt"):
        ps = l.split()

        d = deltas[hex2d[ps[2][-2]]]
        lp = polygon[-1]
        steps = int(ps[2][2:-2], 16)

        p_cnt += steps
        polygon.append((lp[0] + d[0] * steps, lp[1] + d[1] * steps))

    print(shoe_lace(polygon) + (p_cnt + 1) // 2 + 1)


if __name__ == "__main__":
    part1()
    part2()
