import os
import time
import functools
import re

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
    raw_input = "990244-1009337,5518069-5608946,34273134-34397466,3636295061-3636388848,8613701-8663602,573252-688417,472288-533253,960590-988421,7373678538-7373794411,178-266,63577667-63679502,70-132,487-1146,666631751-666711926,5896-10827,30288-52204,21847924-21889141,69684057-69706531,97142181-97271487,538561-555085,286637-467444,93452333-93519874,69247-119122,8955190262-8955353747,883317-948391,8282803943-8282844514,214125-236989,2518-4693,586540593-586645823,137643-211684,33-47,16210-28409,748488-837584,1381-2281,1-19"
    return [tuple(map(int, p.split("-"))) for p in raw_input.strip().split(",")]


def is_invalid_id(num: int) -> bool:
    """Check if the ID is invalid (consists of a sequence repeated twice)."""
    s = str(num)
    length = len(s)
    if length % 2 != 0:
        return False
    half = length // 2
    return s[:half] == s[half:]


@timer
def part_1(data: list[tuple[int, int]]) -> int:
    """Calculate the solution for Part 1."""
    total_invalid_sum = 0
    ranges = data

    for start, end in ranges:
        for num in range(start, end + 1):
            if is_invalid_id(num):
                total_invalid_sum += num

    return total_invalid_sum


def is_invalid_2(num: int) -> bool:
    """Check if the ID is invalid (consists of a sequence repeated at least twice)."""
    return bool(re.match(r"^(.+)\1+$", str(num)))


@timer
def part_2(data: list[tuple[int, int]]) -> int:
    """Calculate the solution for Part 2."""
    total_invalid_sum = 0
    for start, end in data:
        for num in range(start, end + 1):
            if is_invalid_2(num):
                total_invalid_sum += num
    return total_invalid_sum


def main():
    """Execute the solution for both parts."""
    input_data = read_input()

    part_1(input_data)
    part_2(input_data)


if __name__ == "__main__":
    main()
