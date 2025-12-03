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
    max_seen = data[-1]
    for x in reversed(data[:-1]):
        max_val = max(max_val, 10 * x + max_seen)
        max_seen = max(max_seen, x)
    return max_val


@timer
def part_1(data: list[list[int]]) -> int:
    """Calculate the solution for Part 1."""
    return sum(map(ge_max_val, data))


def get_max_12(digits):
    """Find the largest 12-digit number subsequence using a greedy approach."""
    n = len(digits)
    result = 0
    current_idx = 0
    for k in range(12, 0, -1):
        window = digits[current_idx : n - k + 1]
        max_d = max(window)
        result = result * 10 + max_d
        current_idx += window.index(max_d) + 1
    return result


@timer
def part_2(data: list[list[int]]) -> int:
    """Calculate the solution for Part 2."""
    return sum(map(get_max_12, data))


def main():
    """Execute the solution for both parts."""
    input_data = read_input()
    part_1(input_data)
    part_2(input_data)


if __name__ == "__main__":
    main()
