import time
import re
import math
from itertools import combinations


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print(
            "Method "
            + method.__name__
            + " took : "
            + "{:2.5f}".format(time.time() - t)
            + " sec"
        )
        return ret

    return wrapper_method


def mag(v):
    return abs(v[0]) + abs(v[1]) + abs(v[2])


@profiler
def part1():

    ps = []
    for l in open("day20/input.txt"):
        nums = re.findall(r"(-?\d+)", l)
        pos = (int(nums[0]), int(nums[1]), int(nums[2]))
        vel = (int(nums[3]), int(nums[4]), int(nums[5]))
        acc = (int(nums[6]), int(nums[7]), int(nums[8]))

        ps.append([pos, vel, acc])

    print(sorted([(mag(p[2]), mag(p[1]), i) for i, p in enumerate(ps)])[0][2])


def will_collide(d01, v1, a1, d02, v2, a2):
    # d1 = d01 + v1*t + 1/2 * a1 *t*t
    # d2 = d02 + v2*t + 1/2 * a2 *t*t
    # will collide if there is a +ve t for d1 = d2
    # (a2 - a1) * t * t + 2*(v2 - v1) + 2 (d02 - d01) = 0

    a = a2 - a1
    b = 2 * (v2 - v1)
    c = 2 * (d02 - d01)

    if a == 0:
        if b == 0:
            return False
        else:
            return (-c / b) > 0

    if b**2 < 4*a*c:
        return False
    sq = math.sqrt(b**2 - 4 * a * c)
    return ((-b - sq) / (2*a)) > 0 or ((-b + sq) / (2*a)) > 0


@profiler
def part2():

    ps = []
    for l in open("day20/input.txt"):
        nums = re.findall(r"(-?\d+)", l)
        pos = (int(nums[0]), int(nums[1]), int(nums[2]))
        vel = (int(nums[3]), int(nums[4]), int(nums[5]))
        acc = (int(nums[6]), int(nums[7]), int(nums[8]))

        ps.append((pos, vel, acc))

    current_ps = set(ps)
    sim_ps = set()

    t = 0
    while True:

        if len(sim_ps) == len(current_ps):
            for p1, p2 in combinations(sim_ps):
                break
        current_ps


if __name__ == "__main__":

    part1()
    part2()
