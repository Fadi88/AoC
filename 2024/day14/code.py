# pylint: disable=C0114,C0116,C0301,C0209,W1514,C0414


from time import perf_counter_ns
from typing import Any
import os
import re

input_file = os.path.join(os.path.dirname(__file__), "input.txt")
# input_file = os.path.join(os.path.dirname(__file__), "test.txt")


def profiler(method):

    def wrapper_method(*args: Any, **kwargs: Any) -> Any:
        start_time = perf_counter_ns()
        ret = method(*args, **kwargs)
        stop_time = perf_counter_ns() - start_time
        time_len = min(9, ((len(str(stop_time))-1)//3)*3)
        time_conversion = {9: 'seconds', 6: 'milliseconds',
                           3: 'microseconds', 0: 'nanoseconds'}
        print(f"Method {method.__name__} took : {
              stop_time / (10**time_len)} {time_conversion[time_len]}")
        return ret

    return wrapper_method


def simulate_robots(robots, t=100):
    max_x = 101
    max_y = 103

    new_robots = []
    for (rx, ry), (vx, vy) in robots:
        new_robots.append(((rx + t*vx) % max_x, (ry + t*vy) % max_y))
    return new_robots


def count_quadrant(robots):
    c1, c2, c3, c4 = 0, 0, 0, 0
    max_x = 101
    max_y = 103

    for r in robots:
        if r[0] < max_x//2 and r[1] < max_y//2:
            c1 += 1
        elif r[0] > max_x//2 and r[1] < max_y//2:
            c2 += 1
        elif r[0] < max_x//2 and r[1] > max_y//2:
            c3 += 1
        elif r[0] > max_x//2 and r[1] > max_y//2:
            c4 += 1

    return c1*c2*c3*c4


@profiler
def part_1():
    robots = []
    with open(input_file) as f:
        for l in f:
            p = list(map(int, re.findall(r"-?\d+", l)))
            robots.append(((p[0], p[1]), (p[2], p[3])))

    robots = simulate_robots(robots, 100)

    print(count_quadrant(robots))


def count_in_formation(robots):
    deltas = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    touching = 0
    for r in robots:
        for dx, dy in deltas:
            if (r[0]+dx, r[1]+dy) in robots:
                touching += 1
                break
    return touching


@profiler
def part_2():
    robots = []
    with open(input_file) as f:
        for l in f:
            p = list(map(int, re.findall(r"-?\d+", l)))
            robots.append(((p[0], p[1]), (p[2], p[3])))

    t = 1
    while len(set(simulate_robots(robots, t))) != len(robots):
        t += 1
    print(t)

    t = 1
    while count_in_formation(set(simulate_robots(robots, t))) < len(robots) // 2:
        t += 1
    print(t)


if __name__ == "__main__":
    part_1()
    part_2()
