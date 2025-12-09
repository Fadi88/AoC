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


def parse_tiles(data: str) -> list[tuple[int, int]]:
    """Parse input data into a list of coordinate tuples."""
    tiles = []
    for line in data.splitlines():
        parts = line.split(",")
        tiles.append((int(parts[0]), int(parts[1])))
    return tiles


def get_normalized_edges(
    tiles: list[tuple[int, int]],
) -> list[tuple[int, int, int, int]]:
    """Convert tiles into a list of normalized edge tuples (min_x, min_y, max_x, max_y)."""
    edges = []
    n = len(tiles)
    for i in range(n - 1):
        p1 = tiles[i]
        p2 = tiles[i + 1]
        edges.append(
            (
                min(p1[0], p2[0]),
                min(p1[1], p2[1]),
                max(p1[0], p2[0]),
                max(p1[1], p2[1]),
            )
        )

    p_last = tiles[-1]
    p_first = tiles[0]
    edges.append(
        (
            min(p_last[0], p_first[0]),
            min(p_last[1], p_first[1]),
            max(p_last[0], p_first[0]),
            max(p_last[1], p_first[1]),
        )
    )
    return edges


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


def is_fully_contained(
    edges: list[tuple[int, int, int, int]],
    min_x: int,
    min_y: int,
    max_x: int,
    max_y: int,
) -> bool:
    """Check if the rectangle is fully contained."""
    for e_min_x, e_min_y, e_max_x, e_max_y in edges:
        if min_x < e_max_x and max_x > e_min_x and min_y < e_max_y and max_y > e_min_y:
            return False
    return True


@timer
def part2_opt(data: str) -> int:
    """Find the largest rectangle fully contained within the polygon."""
    tiles = parse_tiles(data)
    edges = get_normalized_edges(tiles)

    result = 0

    for p1, p2 in combinations(tiles, 2):
        area = (abs(p1[0] - p2[0]) + 1) * (abs(p1[1] - p2[1]) + 1)
        if area <= result:
            continue

        min_x, max_x = (p1[0], p2[0]) if p1[0] < p2[0] else (p2[0], p1[0])
        min_y, max_y = (p1[1], p2[1]) if p1[1] < p2[1] else (p2[1], p1[1])

        if is_fully_contained(edges, min_x, min_y, max_x, max_y):
            result = area

    return result


def main():
    """Execute the solution for both parts."""
    input_data = read_input()
    part_1(input_data)
    part_2(input_data)
    part2_opt(input_data)


if __name__ == "__main__":
    main()
