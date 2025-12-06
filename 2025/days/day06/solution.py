"""
Advent of Code 2025 - Day 6
"""

import os
import time
import functools
import math

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

    add_lists = [
        [int(row[i]) for row in rows if i < len(row)]
        for i in range(len(rows[0]))
        if ops[i] == "+"
    ]

    mul_lists = [
        [int(row[i]) for row in rows if i < len(row)]
        for i in range(len(rows[0]))
        if ops[i] == "*"
    ]

    add_total = sum(sum(nums) for nums in add_lists)
    mul_total = sum(math.prod(nums) for nums in mul_lists)

    return add_total + mul_total


def transpose(data: str) -> list:
    """Transpose the input, reading columns right-to-left."""
    data = data.split("\n")
    data[-1] += " "
    return ["".join(x) for x in zip(*data)]


def calc_op(op: list) -> int:
    """Calculate the value of an operation array."""
    operator = op[0][-1]

    numbers = []
    for item in op:
        num_str = item.rstrip("+*")
        if num_str.strip():
            numbers.append(int(num_str))
    if operator == "+":
        return sum(numbers)
    elif operator == "*":
        return math.prod(numbers)
    return 0


@timer
def part_2(data: str) -> int:
    """Calculate the solution for Part 2."""
    f = transpose(data)

    ops = []
    current_group = []
    for item in f:
        if item.strip():
            current_group.append(item.strip())
        elif current_group:
            ops.append(current_group)
            current_group = []
    if current_group:
        ops.append(current_group)

    return sum(map(calc_op, ops))


def main():
    """Execute the solution for both parts."""
    input_data = read_input()
    part_1(input_data)
    part_2(input_data)


if __name__ == "__main__":
    main()
