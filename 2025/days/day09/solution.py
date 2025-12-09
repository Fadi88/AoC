"""
Advent of Code 2025 - Day 9
"""

import functools
import os
import time
from itertools import combinations

from shapely.geometry import Polygon, box
from shapely.prepared import prep


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


def calculate_area(p1: tuple[int, int], p2: tuple[int, int]) -> int:
    """Calculate rectangle area including both corners."""
    return (abs(p2[0] - p1[0]) + 1) * (abs(p2[1] - p1[1]) + 1)


@timer
def part_1(data: str) -> int:
    """Find the largest rectangle using any two red tiles as opposite corners."""
    tiles = [tuple(map(int, line.split(","))) for line in data.splitlines() if line]
    return max(calculate_area(p1, p2) for p1, p2 in combinations(tiles, 2))


@timer
def part_2(data: str) -> int:
    """Find the largest rectangle fully contained within the polygon."""
    tiles = [tuple(map(int, line.split(","))) for line in data.splitlines() if line]
    polygon = Polygon(tiles)
    prepared_polygon = prep(polygon)

    max_area = 0
    for p1, p2 in combinations(tiles, 2):
        area = calculate_area(p1, p2)
        if area <= max_area:
            continue

        rectangle = box(
            min(p1[0], p2[0]), min(p1[1], p2[1]), max(p1[0], p2[0]), max(p1[1], p2[1])
        )
        if prepared_polygon.contains(rectangle):
            max_area = area

    return max_area


def main():
    """Execute the solution for both parts."""
    input_data = read_input()
    part_1(input_data)
    part_2(input_data)


if __name__ == "__main__":
    main()
