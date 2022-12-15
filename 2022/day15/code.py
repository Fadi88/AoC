#from time import perf_counter
import re
from time import time as perf_counter


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print('Method ' + method.__name__ + ' took : ' +
              "{:2.5f}".format(perf_counter()-t) + ' sec')
        return ret
    return wrapper_method


def get_taxi_distance(b, s):
    return abs(b[0] - s[0]) + abs(b[1] - s[1])


@profiler
def part1():
    grid = []
    for l in open("input.txt").readlines():
        ps = list(map(int, re.findall(r"-?\d+", l)))
        grid.append(((ps[0], ps[1]), (ps[2], ps[3])))

    ranges = []
    target_y = 2000000

    for s, b in grid:
        d = get_taxi_distance(s, b)

        dy = abs(s[1] - target_y)
        if dy <= d:
            dx = d - dy
            ranges.append((s[0] - dx, s[0] + dx))

    ranges.sort()

    combined_ranges = [ranges[0]]

    for r in ranges[1:]:
        if r[0] > combined_ranges[-1][1]:
            combined_ranges.append(r)
        else:
            combined_ranges[-1] = (combined_ranges[-1][0],
                                   max([combined_ranges[-1][1], r[1]]))

    confirmed = 0

    for r in combined_ranges:
        confirmed += (r[1] - r[0])

    print(confirmed)


@profiler
def part2():
    grid = []
    for l in open("input.txt").readlines():
        ps = list(map(int, re.findall(r"-?\d+", l)))
        grid.append(((ps[0], ps[1]), (ps[2], ps[3])))

    for y in range(0, 4000000):
        free_xs = []
        for s, b in grid:

            d = get_taxi_distance(s, b)
            dy = abs(s[1] - y)
            if dy <= d:
                dx = d - dy
                free_xs.append(
                    (max([s[0] - dx, 0]), min([s[0] + dx, 4000000])))

        free_xs.sort()
        combined_ranges = [free_xs[0]]

        for r in free_xs[1:]:
            if r[0] > combined_ranges[-1][1]:
                combined_ranges.append(r)
            else:
                combined_ranges[-1] = (combined_ranges[-1][0],
                                       max([combined_ranges[-1][1], r[1]]))
        if len(combined_ranges) > 1 or (combined_ranges[0][0] > 0 and combined_ranges[0][1] > 4000000):
            if len(combined_ranges) == 1:
                x = 0 if combined_ranges[0][0] > 0 else 4000000
                # assert that only one slot exist
                assert(combined_ranges[0][0] == 0 != combined_ranges[0][1] == 4000000)
            else:
                x = combined_ranges[0][1] + 1
                # assert that only one slot exist
                assert(x == combined_ranges[1][0] - 1)

            print(x*4000000+y)
            break


if __name__ == "__main__":

    part1()
    part2()
