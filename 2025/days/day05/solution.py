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


def in_range(m: list[tuple[int, int]], x: int) -> bool:
    """Binary search to check if x is in any range in m."""
    l, r = 0, len(m) - 1
    i = -1
    while l <= r:
        mid = (l + r) // 2
        if m[mid][0] <= x:
            i = mid
            l = mid + 1
        else:
            r = mid - 1
    return m[i][0] <= x <= m[i][1]


@timer
def part_1(data: str) -> int:
    """Calculate the solution for Part 1."""
    sec = data.split("\n\n")

    r = [tuple(map(int, line.split("-"))) for line in sec[0].split("\n")]
    d = list(map(int, sec[1].split("\n")))

    r.sort()
    m = [r[0]]
    for s, e in r[1:]:
        if m[-1][1] >= s:
            m[-1] = (m[-1][0], max(m[-1][1], e))
        else:
            m.append((s, e))
    return sum(in_range(m, x) for x in d)


@timer
def part_2(data: str) -> int:
    """Calculate the solution for Part 2."""
    sec = data.split("\n\n")
    r = [tuple(map(int, line.split("-"))) for line in sec[0].split("\n")]
    r.sort()
    m = [r[0]]
    for s, e in r[1:]:
        if m[-1][1] >= s:
            m[-1] = (m[-1][0], max(m[-1][1], e))
        else:
            m.append((s, e))
    return sum(e - s + 1 for s, e in m)


def main():
    """Execute the solution for both parts."""
    input_data = read_input()
    part_1(input_data)
    part_2(input_data)


if __name__ == "__main__":
    main()
