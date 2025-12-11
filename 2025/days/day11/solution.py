"""
Advent of Code 2025 - Day 11
"""

import os
import time
import functools
from collections import defaultdict
from functools import cache

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


grid = defaultdict(list)


@cache
def count_paths(curr, target):
    """Count paths from curr to target using DFS with memoization."""
    if curr == target:
        return 1
    total = 0
    for nxt in grid[curr]:
        total += count_paths(nxt, target)

    return total


def parse_input(data: str):
    """Parse input data into the global grid."""
    grid.clear()
    for l in data.splitlines():
        ps = l.split(": ")
        grid[ps[0]].extend(ps[1].split())


@timer
def part_1(_data: str) -> int:
    """Calculate the solution for Part 1."""
    return count_paths("you", "out")


@timer
def part_2(_data: str) -> int:
    """Calculate the solution for Part 2."""
    p1 = (
        count_paths("svr", "dac")
        * count_paths("dac", "fft")
        * count_paths("fft", "out")
    )

    p2 = (
        count_paths("svr", "fft")
        * count_paths("fft", "dac")
        * count_paths("dac", "out")
    )

    return p1 + p2


def main():
    """Execute the solution for both parts."""
    input_data = read_input()
    parse_input(input_data)
    part_1(input_data)
    part_2(input_data)


if __name__ == "__main__":
    main()
