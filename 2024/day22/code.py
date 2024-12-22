# pylint: disable=C0114,C0116,C0301,C0209,W1514,C0414,E0001

from typing import Any
import os
from time import perf_counter_ns
from collections import defaultdict

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


def gen_new(n):
    n ^= n * 64
    n %= 16777216

    n ^= n // 32
    n %= 16777216

    n ^= n * 2048
    n %= 16777216

    return n


@profiler
def part_1():
    with open(input_file) as f:
        data = list(map(int, f.read().splitlines()))

    for _ in range(2000):
        data = [gen_new(n) for n in data]

    print(sum(data))


def get_deltas(n):
    deltas = []

    for _ in range(2000):
        new_n = gen_new(n)

        b = n % 10
        nb = new_n % 10

        deltas.append((nb-b, nb))

        n = new_n

    return deltas


@profiler
def part_2():
    with open(input_file) as f:
        data = list(map(int, f.read().splitlines()))

    patterns_roi = defaultdict(int)

    for init in data:
        deltas = get_deltas(init)
        added = set()
        for idx in range(len(deltas) - 4):
            pat = tuple(d[0] for d in deltas[idx:idx+4])
            if pat not in added:
                patterns_roi[tuple(pat)] += deltas[idx+3][1]
                added.add(pat)

    print(max(patterns_roi.values()))


if __name__ == "__main__":
    part_1()
    part_2()
