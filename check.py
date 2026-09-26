"""
Checks that every Advent of Code year in the repository has a solution for
each day, and that Python solutions define the expected part functions.

Supported layouts:

    2015/day01/code.py            Python (2015-2024)
    2019/day01/day.cpp            C++ (2018, 2019)
    2021/day01/main.rs            Rust (2021-2024)
    2025/days/day01/solution.py   Python + Rust workspace (2025+)
    2025/days/day01/src/lib.rs

Days may be named day01 or day1. The final day of each year only has one
part, so only part 1 is required there. A single function solving both
parts (e.g. both_part or part_1_2) is also accepted.

Usage: python check.py
"""

import ast
import os
import re

PYTHON_FILES = ("code.py", "solution.py")
SOLUTION_EXTENSIONS = (".py", ".cpp", ".rs", ".go")
# Some days solve both parts in a single function.
COMBINED_PART_FUNCTIONS = {"both_part", "both_parts", "part_1_2", "part12"}
# Starting in 2025, Advent of Code runs for 12 days instead of 25.
SHORT_EVENT_FROM = 2025


def days_in_year(year):
    """Returns the number of puzzle days for the given year."""
    return 12 if year >= SHORT_EVENT_FROM else 25


def find_years(project_path):
    """Returns the sorted list of year folders in the project."""
    return sorted(
        int(name)
        for name in os.listdir(project_path)
        if re.fullmatch(r"\d{4}", name)
        and os.path.isdir(os.path.join(project_path, name))
    )


def find_day_dir(year_path, day):
    """Returns the folder for a day, or None if it does not exist."""
    for parent in (os.path.join(year_path, "days"), year_path):
        for name in (f"day{day:02d}", f"day{day}"):
            path = os.path.join(parent, name)
            if os.path.isdir(path):
                return path
    return None


def has_solution(day_path):
    """Checks whether a day folder contains any solution source file."""
    for _, _, files in os.walk(day_path):
        if any(f.endswith(SOLUTION_EXTENSIONS) for f in files):
            return True
    return False


def check_python_parts(py_path, last_day, errors):
    """Checks that a Python solution defines the required part functions."""
    try:
        with open(py_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())
    except SyntaxError as e:
        errors["syntax_errors"].append(f"{py_path}: {e}")
        return

    names = {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }

    if names & COMBINED_PART_FUNCTIONS:
        return

    required = [1] if last_day else [1, 2]
    for part in required:
        if f"part{part}" not in names and f"part_{part}" not in names:
            errors["missing_functions"].append(
                f"Missing 'part{part}' or 'part_{part}' in {py_path}"
            )


def check_day(year, day, year_path, errors):
    """Checks a single day for completeness."""
    day_path = find_day_dir(year_path, day)
    if day_path is None:
        errors["missing_folders"].append(f"{year}/day{day:02d}")
        return

    if not has_solution(day_path):
        errors["missing_files"].append(f"No solution file in {day_path}")
        return

    for name in PYTHON_FILES:
        py_path = os.path.join(day_path, name)
        if os.path.exists(py_path):
            check_python_parts(py_path, day == days_in_year(year), errors)


def check_project_completeness(project_path):
    """Checks every year in the project and prints any problems found."""
    errors = {
        "missing_folders": [],
        "missing_files": [],
        "missing_functions": [],
        "syntax_errors": [],
    }

    years = find_years(project_path)
    for year in years:
        year_path = os.path.join(project_path, str(year))
        for day in range(1, days_in_year(year) + 1):
            check_day(year, day, year_path, errors)

    titles = {
        "missing_folders": "Missing day folders",
        "missing_files": "Missing solution files",
        "missing_functions": "Missing functions",
        "syntax_errors": "Syntax errors",
    }
    for key, title in titles.items():
        if errors[key]:
            print(f"{title}:")
            for item in errors[key]:
                print(f"  - {item}")
            print()

    if not any(errors.values()):
        print(f"All good: checked {len(years)} years ({years[0]}-{years[-1]}).")
        return True
    return False


if __name__ == "__main__":
    import sys

    sys.exit(0 if check_project_completeness(".") else 1)
