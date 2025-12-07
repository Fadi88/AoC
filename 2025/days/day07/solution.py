"""
Advent of Code 2025 - Day 7
"""

import os
import time
import functools
from collections import defaultdict

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
    lines = data.splitlines()
    h = len(lines)

    grid = set()
    s = (0, 0)

    for y, l in enumerate(lines):
        for x, c in enumerate(l):
            if c == "^":
                grid.add((x, y))
            elif c == "S":
                s = (x, y)

    total = 0
    tips = {s[0]}

    for y in range(s[1] + 1, h):
        # Optimization: If no beam hits a splitter, they all just fall straight down.
        if not any((x, y) in grid for x in tips):
            continue

        next_tips = set()
        for x in tips:
            if (x, y) in grid:
                total += 1
                next_tips.add(x - 1)
                next_tips.add(x + 1)
            else:
                next_tips.add(x)

        tips = next_tips
        if not tips:
            break

    return total


@timer
def part_2(data: str) -> int:
    """Calculate the solution for Part 2."""
    lines = data.splitlines()
    h = len(lines)

    # Parse Grid
    grid = set()
    s = (0, 0)

    for y, l in enumerate(lines):
        for x, c in enumerate(l):
            if c == "^":
                grid.add((x, y))
            elif c == "S":
                s = (x, y)

    tips = defaultdict(int)
    tips[s[0]] = 1

    for y in range(s[1] + 1, h):
        # Optimization: Keys (beams) fall straight unless hitting a splitter
        if not any((x, y) in grid for x in tips):
            continue

        next_tips = defaultdict(int)
        for x, count in tips.items():
            if (x, y) in grid:
                next_tips[x - 1] += count
                next_tips[x + 1] += count
            else:
                next_tips[x] += count

        tips = next_tips
        if not tips:
            break

    return sum(tips.values())


def main():
    """Execute the solution for both parts."""
    input_data = read_input()
    part_1(input_data)
    part_2(input_data)


if __name__ == "__main__":
    main()
