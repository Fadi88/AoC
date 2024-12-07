# pylint: disable=C0114,C0116,C0301,C0209,W1514,C0414

from time import time as perf_counter
from itertools import product
from typing import Any
import math


def profiler(method):
    def wrapper_method(*args: Any, **kwargs: Any) -> Any:
        t = perf_counter()
        ret = method(*args, **kwargs)
        print(f"Method {method.__name__} took : {perf_counter() - t:.3f} sec")
        return ret

    return wrapper_method


def eval_right_to_left(nums, target, ops):
    s = nums[0]
    for i in range(len(ops)):
        if ops[i] == "+":
            s += nums[i+1]
        elif ops[i] == "*":
            s *= nums[i+1]
        elif ops[i] == "||":
            s = int(s * 10**int(math.log10(nums[i+1]) + 1) + nums[i+1])

        if s > target:
            return False

    return s == target


def does_match(target, nums, ops):
    for op in product(ops, repeat=len(nums) - 1):
        if eval_right_to_left(nums, target, op):
            return True
    return False


@profiler
def part1():

    cals = []
    with open("day07/input.txt") as f:
        for l in f:
            ps = l.strip().split(":")
            cals.append((int(ps[0]), list(map(int, ps[1].split()))))

    print(sum(v for v, nums in cals if does_match(v, nums, ["+", "*"])))


@profiler
def part2():

    cals = []
    with open("day07/input.txt") as f:
        for l in f:
            ps = l.strip().split(":")
            cals.append((int(ps[0]), list(map(int, ps[1].split()))))

    print(sum(v for v, nums in cals if does_match(v, nums, ["+", "*", "||"])))


if __name__ == "__main__":
    part1()
    part2()
