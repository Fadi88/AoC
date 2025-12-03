"""
Advent of Code 2025 - Day 3
"""

import os
import time
import functools

# pylint: disable=fixme


def timer(func):
    """Decorator to measure the execution time of a function."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper function to execute the decorated function and print its runtime."""
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"[{func.__name__}] Result: {result}")
        duration = end - start
        time_units = {
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


def read_input():
    """Read and parse the input file."""
    input_path = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(input_path, "r", encoding="utf-8") as f:
        return [list(map(int, line.strip())) for line in f]


def ge_max_val(data):
    """Find the largest 2-digit number subsequence using a single pass."""
    max_val = 0
    max_seen = -1
    for x in reversed(data):
        if max_seen != -1:
            max_val = max(max_val, 10 * x + max_seen)
        max_seen = max(max_seen, x)
    return max_val


@timer
def part_1(data: list[list[int]]) -> int:
    """Calculate the solution for Part 1."""
    return sum(map(ge_max_val, data))


def get_max_dp(digits: list[int]) -> int:
    """Find the largest 12-digit number subsequence using DP."""
    n = len(digits)

    @functools.cache
    def dp(index, k):
        if k == 1:  # only 1 digit left pick the max
            return max(digits[index:])
        pick = digits[index] * (10 ** (k - 1)) + dp(index + 1, k - 1)
        if n - index == k:
            return pick

        skip = dp(index + 1, k)
        return max(pick, skip)

    return dp(0, 12)


@timer
def part_2(data: list[list[int]]) -> int:
    """Calculate the solution for Part 2."""
    total = 0
    for bank in data:
        total += get_max_dp(bank)
    return total


def main():
    """Execute the solution for both parts."""
    input_data = read_input()
    part_1(input_data)
    part_2(input_data)


if __name__ == "__main__":
    main()
