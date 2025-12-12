"""
Advent of Code 2025 - Day 12
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


def is_region_valid(region: str, shapes: list[tuple[int, int]]) -> bool:
    """Check if a region is valid."""
    ds, req = region.split(": ")
    w, h = ds.split("x")
    available_size = int(w) * int(h)
    required_gifts = list(map(int, req.split(" ")))
    required_size = sum(q * shapes[i][1] for i, q in enumerate(required_gifts))
    return available_size >= required_size


@timer
def part_1(data: str) -> int:
    """Calculate the solution for Part 1."""
    ps = data.split("\n\n")

    shapes = []
    for p in ps[:-1]:
        lines = "".join(p.split("\n")[1:]).replace("\n", "")
        shapes.append(
            (int(lines.replace("#", "1").replace(".", "0"), 2), lines.count("#"))
        )

    return sum(is_region_valid(region, shapes) for region in ps[-1].split("\n"))


def main():
    """Execute the solution for both parts."""
    input_data = read_input()
    part_1(input_data)


if __name__ == "__main__":
    main()
