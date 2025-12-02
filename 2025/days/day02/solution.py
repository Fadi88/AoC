"""
Advent of Code 2025 - Day 2 Solution
"""

import os
import time
import functools
import re
import math

# pylint: disable=fixme


import sys

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from utils.decorators import timer


def read_input():
    """Read and parse the input file."""
    input_path = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(input_path, "r", encoding="utf-8") as f:
        return [p.split("-") for p in f.read().strip().split(",")]


def is_invalid_id(num: int) -> bool:
    """Check if the ID is invalid (consists of a sequence repeated twice)."""
    s = str(num)
    l = len(s)
    if l % 2 != 0:
        return False
    mid = l // 2
    return s[:mid] == s[mid:]


@timer
def part_1(data: list[list[str]]) -> int:
    """Calculate the solution for Part 1."""
    s = 0
    for start, end in data:
        for num in range(int(start), int(end) + 1):
            if is_invalid_id(num):
                s += num

    return s


def is_invalid_2(num: int) -> bool:
    """Check if the ID is invalid (consists of a sequence repeated at least twice)."""
    return bool(re.match(r"^(.+)\1+$", str(num)))


@timer
def part_2(data: list[list[str]]) -> int:
    """Calculate the solution for Part 2."""
    s = 0
    for start, end in data:
        for num in range(int(start), int(end) + 1):
            if is_invalid_2(num):
                s += num
    return s


def is_invalid_2_opt(num: int) -> bool:
    """Check if the ID is invalid using first digit repetition"""
    s = str(num)
    l = len(s)
    ff = s.count(s[0])

    common = math.gcd(l, ff)

    if common < 2:
        return False

    for k in range(common, 1, -1):
        if common % k == 0:
            d = l // k
            if s == s[:d] * k:
                return True
    return False


@timer
def part_2_opt(data: list[list[str]]) -> int:
    """Calculate the solution for Part 2 using optimized check."""
    s = 0
    for start, end in data:
        for num in range(int(start), int(end) + 1):
            if is_invalid_2_opt(num):
                s += num
    return s


if __name__ == "__main__":

    input_data = read_input()

    part_1(input_data)
    part_2(input_data)
    part_2_opt(input_data)
