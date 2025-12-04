"""
Advent of Code 2025 - Day 4
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
    paper = set()
    with open(input_path, "r", encoding="utf-8") as f:
        for y, l in enumerate(f.read().strip().split("\n")):
            for x, c in enumerate(l):
                if c == "@":
                    paper.add((x, y))
    return paper


def count_neighbors(x, y, paper):
    """Count the number of adjacent paper rolls."""
    count = 0
    ds = [-1, 0, 1]
    for dx in ds:
        for dy in ds:
            if dx == dy == 0:
                continue
            if (x + dx, y + dy) in paper:
                count += 1
    return count


@timer
def part_1(data: set[tuple[int, int]]) -> int:
    """Calculate the solution for Part 1."""
    paper = data
    count = 0
    for x, y in paper:
        if count_neighbors(x, y, paper) < 4:
            count += 1
    return count


@timer
def part_2(data: set[tuple[int, int]]) -> int:
    """Calculate the solution for Part 2."""
    paper = data.copy()
    total_removed = 0
    while True:
        to_remove = {(x, y) for x, y in paper if count_neighbors(x, y, paper) < 4}

        if not to_remove:
            break

        total_removed += len(to_remove)
        paper -= to_remove

    return total_removed


def main():
    """Execute the solution for both parts."""
    input_data = read_input()
    part_1(input_data)
    part_2(input_data)


if __name__ == "__main__":
    main()
