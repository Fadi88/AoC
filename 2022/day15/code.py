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

    confirmed_free = []
    target_y = 2000000

    for sensor, beacon in grid:
        b_s_dst = get_taxi_distance(sensor, beacon)

        dy = abs(sensor[1] - target_y)
        if dy <= b_s_dst:
            dx = b_s_dst - dy
            confirmed_free.append((sensor[0] - dx, sensor[0] + dx))

    confirmed_free.sort()

    combined_ranges = [confirmed_free[0]]

    for r in confirmed_free[1:]:
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
        for sensor, beacon in grid:

            b_s_dst = get_taxi_distance(sensor, beacon)
            dy = abs(sensor[1] - y)
            if dy <= b_s_dst:
                dx = b_s_dst - dy
                free_xs.append(
                    (max([sensor[0] - dx, 0]), min([sensor[0] + dx, 4000000])))

        free_xs.sort()
        combined_ranges = [free_xs[0]]

        for r in free_xs[1:]:
            to_check = combined_ranges[-1]
            if r[0] > to_check[1]:
                combined_ranges.append(r)
            else:
                combined_ranges[-1] = (to_check[0], max([to_check[1], r[1]]))

        if len(combined_ranges) > 1 or (combined_ranges[0][0] > 0 and combined_ranges[0][1] > 4000000):
            # a gap exists in the range
            if len(combined_ranges) == 1:
                # the gap is at one of the extremities 
                x = 0 if combined_ranges[0][0] > 0 else 4000000
                
                # assert that only one slot exist
                assert(combined_ranges[0][0] == 0 !=
                       combined_ranges[0][1] == 4000000)
            else:
                # the gap is in the middle
                x = combined_ranges[0][1] + 1
                
                # assert that only one slot exist
                assert(x == combined_ranges[1][0] - 1)

            print(x*4000000+y)
            break


if __name__ == "__main__":

    part1()
    part2()
