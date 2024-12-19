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


count = {}


def count_allowed(towel, patterns):
    combs = 0
    if towel in count:
        return count[towel]

    for p in patterns:
        if towel == p:
            combs += 1
        if towel.startswith(p):
            new_towel = towel.replace(p, "", 1)
            combs += count_allowed(new_towel, patterns)
    count[towel] = combs
    return combs


@profiler
def part_1():
    with open(input_file) as f:
        ps = f.read().split("\n\n")

    allowed = list(ps[0].split(", "))
    towels = ps[1].split()

    print(sum(count_allowed(t, allowed) > 0 for t in towels))


@profiler
def part_2():
    with open(input_file) as f:
        ps = f.read().split("\n\n")

    allowed = list(ps[0].split(", "))
    allowed.sort(key=lambda x: -len(x))

    towels = ps[1].split()

    print(sum(count_allowed(t, allowed) for t in towels))


if __name__ == "__main__":
    part_1()
    part_2()
