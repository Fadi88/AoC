# pylint: disable=C0114,C0116,C0301,C0209,W1514,C0414,C0200,E0001

from time import perf_counter_ns
import os
from typing import Any

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


def maze(pts):
    start = (0, 0)
    end = (70, 70)

    seen = set()
    to_visit = [(start, 0)]

    while to_visit:
        cp, cd = to_visit.pop(0)

        if cp in seen:
            continue

        if cp == end:
            return cd

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            np = cp[0] + dx, cp[1] + dy
            if 0 <= np[0] <= 70 and 0 <= np[1] <= 70 and np not in seen and np not in pts:
                to_visit.append((np, cd+1))

        seen.add(cp)

    return None


@profiler
def part_1():
    with open(input_file) as f:
        pts = [tuple(map(int, l.strip().split(","))) for l in f]
    print(maze(pts[:1024]))


@profiler
def part_2():
    with open(input_file) as f:
        pts = [tuple(map(int, l.strip().split(","))) for l in f]

    lower = 1024
    upper = len(pts)

    while upper - lower > 1:
        l = (upper+lower) // 2

        if maze(pts[:l]):
            lower = l
        else:
            upper = l

    print(pts[upper-1])


if __name__ == "__main__":
    part_1()
    part_2()
