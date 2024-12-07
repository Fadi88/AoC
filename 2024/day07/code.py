# pylint: disable=C0114,C0116,C0301,C0209,W1514

from time import perf_counter as perf_counter
from typing import Any


def profiler(method):
    def wrapper_method(*args: Any, **kwargs: Any) -> Any:
        t = perf_counter()
        ret = method(*args, **kwargs)
        print(f"Method {method.__name__} took : {perf_counter() - t:.3f} sec")
        return ret

    return wrapper_method


def eval_right_to_left(l: list[int], target: int) -> bool:
    """Evaluates a list of integers from left to right using + and * operations to find a target."""
    if len(l) == 1:
        return l[0] == target

    n = l.pop(0)

    l1 = l.copy()

    l[0] += n
    l1[0] *= n

    return eval_right_to_left(l, target) or eval_right_to_left(l1, target)


@profiler
def part1():
    inp = {}

    cals = []
    with open("day07/input.txt") as f:
        for l in f:
            ps = l.strip().split(":")
            inp[int(ps[0])] = list(map(int, ps[1].split()))
            cals.append((int(ps[0]), list(map(int, ps[1].split()))))

    print(sum(v for v, nums in cals if eval_right_to_left(nums, v)))


def eval_right_to_left_2(numbers: list[int], target: int) -> bool:
    """
    Evaluate the list of numbers from right to left.

    The evaluation is done by applying the operators +, * and ``concat``.
    The ``concat`` operator concatenates the string representation of the
    two numbers.
    """
    if len(numbers) == 1:
        return numbers[0] == target

    n = numbers.pop(0)

    numbers1 = list(numbers)
    numbers2 = list(numbers)
    numbers3 = list(numbers)

    numbers1[0] += n
    numbers2[0] *= n
    numbers3[0] = int(str(n) + str(numbers3[0]))

    return (
        eval_right_to_left_2(numbers1, target)
        or eval_right_to_left_2(numbers2, target)
        or eval_right_to_left_2(numbers3, target)
    )


@profiler
def part2():
    inp = {}

    cals = []
    with open("day07/input.txt") as f:
        for l in f:
            ps = l.strip().split(":")
            inp[int(ps[0])] = list(map(int, ps[1].split()))
            cals.append((int(ps[0]), list(map(int, ps[1].split()))))

    print(sum(v for v, nums in cals if eval_right_to_left_2(nums, v)))


if __name__ == "__main__":
    part1()
    part2()
