# pylint: disable=C0114,C0116,C0301,C0209,W1514,C0414

from time import time as perf_counter
from typing import Any
import os

input_file = os.path.join(os.path.dirname(__file__), "input.txt")
# input_file = os.path.join(os.path.dirname(__file__), "test.txt")


def profiler(method):
    def wrapper_method(*args: Any, **kwargs: Any) -> Any:
        t = perf_counter()
        ret = method(*args, **kwargs)
        print(f"Method {method.__name__} took : {perf_counter() - t:.3f} sec")
        return ret

    return wrapper_method


@profiler
def part1():
    with open(input_file) as _f:
        pass


@profiler
def part2():
    with open(input_file) as _f:
        pass


if __name__ == "__main__":
    part1()
    part2()
