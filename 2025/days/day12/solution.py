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
    """Check if a region is valid based on area heuristic."""
    dimensions_str, requirements_str = region.split(": ")
    width, height = dimensions_str.split("x")

    available_area = int(width) * int(height)
    required_counts = list(map(int, requirements_str.split(" ")))

    required_area = sum(
        count * shape[1] for count, shape in zip(required_counts, shapes)
    )

    return available_area >= required_area


@timer
def part_1(data: str) -> int:
    """Calculate the solution for Part 1."""
    chunks = data.split("\n\n")
    shape_chunks = chunks[:-1]
    region_chunk = chunks[-1]

    shapes = []
    for chunk in shape_chunks:
        shape_lines = "".join(chunk.split("\n")[1:])
        flattened_shape = shape_lines.replace("\n", "")

        bitmask = int(flattened_shape.translate(str.maketrans("#.", "10")), 2)
        area = flattened_shape.count("#")
        # shape (bitmask for the shape, total occupied area by the shape(number of #))
        shapes.append((bitmask, area))

    valid_region_count = sum(
        is_region_valid(region_line, shapes) for region_line in region_chunk.split("\n")
    )

    return valid_region_count


def main():
    """Execute the solution for both parts."""
    input_data = read_input()
    part_1(input_data)


if __name__ == "__main__":
    main()
