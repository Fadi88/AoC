# pylint: disable=C0114,C0116,C0301,C0209,W1514,C0414

from time import perf_counter as perf_counter
from typing import Any
import math


def profiler(method):
    def wrapper_method(*args: Any, **kwargs: Any) -> Any:
        t = perf_counter()
        ret = method(*args, **kwargs)
        print(f"Method {method.__name__} took : {perf_counter() - t:.3f} sec")
        return ret

    return wrapper_method


def eval_right_to_left_ops(numbers: list[int], target: int, ops: list[callable]) -> bool:
    """Evaluate the given numbers with the given operations from right to left."""
    if len(numbers) == 1:
        return numbers[0] == target
    return any(eval_right_to_left_ops(op(numbers), target, ops) for op in ops)


def op_add(l):
    nl = list(l)
    n = nl.pop(0)

    nl[0] += n
    return nl


def op_mul(l):
    nl = list(l)
    n = nl.pop(0)

    nl[0] *= n
    return nl


@profiler
def part1():

    cals = []
    with open("day07/input.txt") as f:
        for l in f:
            ps = l.strip().split(":")
            cals.append((int(ps[0]), list(map(int, ps[1].split()))))

    ops = [op_add, op_mul]
    print(sum(v for v, nums in cals if eval_right_to_left_ops(nums, v, ops)))


def op_cat(l):
    nl = list(l)
    n = nl.pop(0)

    nl[0] = int(n * 10**int(math.log10(nl[0]) + 1) + nl[0])
    return nl


@profiler
def part2():

    cals = []
    with open("day07/input.txt") as f:
        for l in f:
            ps = l.strip().split(":")
            cals.append((int(ps[0]), list(map(int, ps[1].split()))))

    ops = [op_add, op_mul, op_cat]
    print(sum(v for v, nums in cals if eval_right_to_left_ops(nums, v, ops)))


if __name__ == "__main__":
    part1()
    part2()
