# pylint: disable=C0114,C0116,C0301,C0209,W1514,C0414,C0103

import time
import re
import heapq


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print("Method " + method.__name__ + " took : " +
              "{:2.5f}".format(time.time() - t) + " sec")
        return ret

    return wrapper_method


def get_dst(p1, p2):
    return sum(abs(p1[i] - p2[i]) for i in range(3))


def get_in_range(bots, b):
    return sum(get_dst(p[0], b[0]) <= b[1] for p in bots)


@profiler
def part_1():
    bots = []
    max_b = ((0, 0, 0), -1)
    for l in open("day23/input.txt").read().splitlines():
        p = re.findall(r"-?\d+", l)
        bots.append((((int(p[0]), int(p[1]), int(p[2])), int(p[3]))))
        if int(p[3]) > max_b[1]:
            max_b = bots[-1]

    print(get_in_range(bots, max_b))


@profiler
def part_2():

    h = []

    for l in open("day23/input.txt").read().splitlines():
        p = re.findall(r"-?\d+", l)

        x, y, z, r = int(p[0]), int(p[1]), int(p[2]), int(p[3])
        d = abs(x) + abs(y) + abs(z)

        heapq.heappush(h, (d - r, 1))
        heapq.heappush(h, (d + r, -1))

    count = 0
    max_count = 0
    result = 0

    while h:
        dist, e = heapq.heappop(h)
        count += e
        if count > max_count:
            result = dist
            max_count = count
    print(result)


if __name__ == "__main__":

    part_1()
    part_2()
