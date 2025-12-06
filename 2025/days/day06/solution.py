"""
Advent of Code 2025 - Day 6
"""

import os
import time
import functools
import math
from itertools import zip_longest

# pylint: disable=fixme


def timer(func):
    """Decorator to measure the execution time of a function."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper function to execute the decorated function and print its runtime."""
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"[{func.__name__}] Result: {result}")
        duration = end - start
        time_units = {
            "ns": (1e-6, 1e9),
            "us": (1e-3, 1e6),
            "ms": (1, 1e3),
            "s": (float("inf"), 1),
        }
        for unit, (threshold, multiplier) in time_units.items():
            if duration < threshold:
                print(f"[{func.__name__}] Time: {duration * multiplier:.4f} {unit}")
                break
        return result

    return wrapper


def read_input() -> str:
    """Read and parse the input file."""
    input_path = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(input_path, "r", encoding="utf-8") as f:
        return f.read().strip()


@timer
def part_1(data: str) -> int:
    """Calculate the solution for Part 1."""
    lines = data.split("\n")
    ops = lines[-1].split()
    rows = [line.split() for line in lines[:-1]]

    total = 0
    for i, op in enumerate(ops):
        nums = [int(row[i]) for row in rows if i < len(row)]
        total += sum(nums) if op == "+" else math.prod(nums)
    return total


def transpose(data: str) -> list:
    """Transpose the input, handling uneven line lengths."""
    return ["".join(x) for x in zip_longest(*data.split("\n"), fillvalue=" ")]


def calc_op(op: list) -> int:
    """Calculate the value of an operation array."""
    operator = op[0][-1]
    numbers = [int(item.rstrip("+*")) for item in op if item.rstrip("+*").strip()]
    return sum(numbers) if operator == "+" else math.prod(numbers)


@timer
def part_2(data: str) -> int:
    """Calculate the solution for Part 2."""
    groups = "\n".join(row.strip() for row in transpose(data)).split("\n\n")
    return sum(calc_op(group.splitlines()) for group in groups if group.strip())


def main():
    """Execute the solution for both parts."""
    input_data = read_input()
    part_1(input_data)
    part_2(input_data)


if __name__ == "__main__":
    main()
