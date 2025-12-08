"""
Advent of Code 2025 - Day 8
"""

import itertools
import os
import time
import functools
import heapq

# pylint: disable=fixme


def timer(func):
    """Decorator to time function execution."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"[{func.__name__}] Result: {result}")
        if (duration := end - start) < 1:
            print(f"[{func.__name__}] Time: {duration * 1000:.4f} ms")
        else:
            print(f"[{func.__name__}] Time: {duration:.4f} s")
        return result

    return wrapper


def read_input() -> str:
    """Read input from file."""
    input_path = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(input_path, "r", encoding="utf-8") as f:
        return f.read().strip()


def dist_sq(p1, p2):
    """Calculate squared Euclidean distance between two 3D points."""
    return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2


def get_pairs(points):
    """Generate all pairs of points (unsorted)."""
    return [
        (dist_sq(p1, p2), i, j)
        for (i, p1), (j, p2) in itertools.combinations(enumerate(points), 2)
    ]


@timer
def part_1(data: str) -> int:
    """Solve Part 1: Product of sizes of 3 largest clusters using 1000 closest edges."""
    points = [tuple(map(int, line.split(","))) for line in data.splitlines()]
    pairs = get_pairs(points)

    top_pairs = heapq.nsmallest(1000, pairs, key=lambda x: x[0])

    components = [{i} for i in range(len(points))]

    for _, i, j in top_pairs:
        idx_i = -1
        idx_j = -1

        for idx, comp in enumerate(components):
            if i in comp:
                idx_i = idx
            if j in comp:
                idx_j = idx

        if idx_i != idx_j:
            components[idx_i].update(components[idx_j])
            components.pop(idx_j)

    sizes = sorted([len(c) for c in components], reverse=True)
    return sizes[0] * sizes[1] * sizes[2]


@timer
def part_2(data: str) -> int:
    """Solve Part 2: Product of Xs of last connected points for full connectivity."""
    points = [tuple(map(int, line.split(","))) for line in data.splitlines()]
    pairs = get_pairs(points)

    heapq.heapify(pairs)

    components = [{i} for i in range(len(points))]

    while pairs:
        _, i, j = heapq.heappop(pairs)

        idx_i = -1
        idx_j = -1

        for idx, comp in enumerate(components):
            if i in comp:
                idx_i = idx
            if j in comp:
                idx_j = idx

        if idx_i != idx_j:
            components[idx_i].update(components[idx_j])
            components.pop(idx_j)

            if len(components) == 1:
                return points[i][0] * points[j][0]
    return 0


def main():
    """Run the solution."""
    input_data = read_input()
    part_1(input_data)
    part_2(input_data)


if __name__ == "__main__":
    main()
