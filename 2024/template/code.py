# pylint: disable=C0114,C0116,C0301,C0209,W1514,C0414,E0001

from typing import Any
import os
from time import perf_counter_ns

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


@profiler
def part_1():
    with open(input_file) as _f:
        pass


@profiler
def part_2():
    with open(input_file) as _f:
        pass


if __name__ == "__main__":
    part_1()
    part_2()
