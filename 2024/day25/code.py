# pylint: disable=C0114,C0116,C0301,C0209,W1514,C0414,E0001

from typing import Any
import os
from time import perf_counter_ns
from itertools import product

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


def get_heights(d):
    ret = []
    for i in range(len(d[0])):
        col = [l[i] == "#" for l in d]
        ret.append(sum(col))
    return ret


def does_fit(p):
    ks, ls = p
    return all(k+l <= 7 for k, l in zip(ks, ls))


@profiler
def part_1():
    key_heights = []
    lock_heights = []

    with open(input_file) as f:
        for block in f.read().split("\n\n"):
            lines = block.splitlines()
            if lines[0].count(".") == 0:
                lock_heights.append(get_heights(lines))
            else:
                key_heights.append(get_heights(lines))

    s = sum(does_fit(combination)
            for combination in product(key_heights, lock_heights))
    print(s)


if __name__ == "__main__":
    part_1()
