# pylint: disable=C0114,C0116,C0301,C0209,W1514,C0414

from time import time as perf_counter
from typing import Any
import os
import re

input_file = os.path.join(os.path.dirname(__file__), "input.txt")
# input_file = os.path.join(os.path.dirname(__file__), "test.txt")


def profiler(method):
    from time import perf_counter_ns

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


def solve_linear_system(a, b, p, delta=0):
    ax, ay = a
    bx, by = b
    px, py = p

    px += delta
    py += delta

    n1 = (px*by - py*bx) / (ax*by - ay*bx)
    n2 = (py*ax - px*ay) / (ax*by - ay*bx)

    return n1, n2


@profiler
def part_1():
    with open(input_file) as f:
        l = f.read().split("\n\n")

    machines = []
    for g in l:
        p = list(map(int, re.findall(r"\d+", g)))
        machines.append(((p[0], p[1]), (p[2], p[3]), (p[4], p[5])))

    tokens = 0
    for m in machines:

        n1, n2 = solve_linear_system(m[0], m[1], m[2])

        if n1 % 1 == 0 and n2 % 1 == 0 and 0 <= int(n1) < 100 and 0 <= int(n2) < 100:
            tokens += (3*int(n1) + int(n2))

    print(tokens)


@profiler
def part_2():
    with open(input_file) as f:
        l = f.read().split("\n\n")

    machines = []
    for g in l:
        p = list(map(int, re.findall(r"\d+", g)))
        machines.append(((p[0], p[1]), (p[2], p[3]), (p[4], p[5])))

    tokens = 0
    for m in machines:
        n1, n2 = solve_linear_system(m[0], m[1], m[2], 10000000000000)

        if n1 % 1 == 0 and n2 % 1 == 0 and int(n1) >= 0 and int(n2) >= 0:
            tokens += (3*int(n1) + int(n2))

    print(tokens)


if __name__ == "__main__":
    part_1()
    part_2()
