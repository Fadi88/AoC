"""
Advent of Code 2025 - Day 5
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


def read_input() -> str:
    """Read and parse the input file."""
    input_path = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(input_path, "r", encoding="utf-8") as f:
        return f.read().strip()


@timer
def part_1(data: str) -> int:
    """Calculate the solution for Part 1."""
    sec = data.split("\n\n")
    ranges = sec[0]
    values = sec[1] if len(sec) > 1 else ""

    r = [tuple(map(int, line.split("-"))) for line in ranges.split("\n")]
    r.sort(key=lambda x: x[0])
    m = []
    for s, e in r:
        if m and m[-1][1] >= s:
            m[-1][1] = max(m[-1][1], e)
        else:
            m.append([s, e])
    d = list(map(int, values.split("\n"))) if values else []
    return sum(1 for x in d if any(s <= x <= e for s, e in m))


@timer
def part_2(data: str) -> int:
    """Calculate the solution for Part 2."""
    sec = data.split("\n\n")
    ranges = sec[0]

    r = [tuple(map(int, line.split("-"))) for line in ranges.split("\n")]
    r.sort(key=lambda x: x[0])
    m = []
    for s, e in r:
        if m and m[-1][1] >= s:
            m[-1][1] = max(m[-1][1], e)
        else:
            m.append([s, e])
    return sum(e - s + 1 for s, e in m)


def main():
    """Execute the solution for both parts."""
    input_data = read_input()
    part_1(input_data)
    part_2(input_data)


if __name__ == "__main__":
    main()
