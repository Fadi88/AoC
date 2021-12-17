import time
import re
import math


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


def get_pos(vx0, vy0, t):
    y = vy0 * t - (t - 1) * (t) // 2

    # ignore -ve x as the input is to the right
    x = (2 * vx0 - t + 1) * (t) // 2 if t < vx0 else vx0 * (vx0 + 1) // 2

    return x, y


def will_intersect(v, u, l):
    # get time limit based on y because it is easier to get than x
    # if it works for that time slot for y should also work x
    # because they both has to match
    tmin = math.floor(v[1] + math.sqrt(v[1] * v[1] - 2 * u[1]))
    tmax = math.floor(v[1] + math.sqrt(v[1] * v[1] - 2 * l[1]))

    for t in range(tmin, tmax + 2):
        x, y = get_pos(v[0], v[1], t)
        if u[0] <= x <= l[0] and l[1] <= y <= u[1]:
            return True
    return False


@profiler
def part1():
    _, _, y1, _ = list(map(int, re.findall(r"-?\d+", open("day17/input.txt").read())))

    print(abs(y1) * (abs(y1) - 1) // 2)


@profiler
def part2():
    x1, x2, y1, y2 = list(
        map(int, re.findall(r"-?\d+", open("day17/input.txt").read()))
    )

    # assume area is under y = 0

    # bounds if exceeded after 1 second will overshoot
    vy_min = y1
    vx_max = x2

    vy_max = -y1
    vx_min = math.floor(math.sqrt(2 * x1) - 1)

    upper_bound = (x1, y2)
    lower_bound = (x2, y1)

    tmp = sum(
        [
            will_intersect((vx, vy), upper_bound, lower_bound)
            for vx in range(vx_min, vx_max + 1)
            for vy in range(vy_min, vy_max + 1)
        ]
    )

    print(tmp)


if __name__ == "__main__":

    part1()
    part2()
