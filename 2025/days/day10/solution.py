"""
Advent of Code 2025 - Day 10
"""

import os
import time
import functools
import ast
from collections import deque
import numpy as np
from scipy.optimize import linprog


def timer(func):
    """Decorator to measure the execution time of a function."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
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


def solve_machine(machine):
    """Solve a single machine using bfs."""
    goal, buttons = machine

    queue = deque([(0, 0)])
    visited = {0}

    while queue:
        curr, steps = queue.popleft()
        if curr == goal:
            return steps

        for b_mask in buttons:
            nxt = curr ^ b_mask
            if nxt not in visited:
                visited.add(nxt)
                queue.append((nxt, steps + 1))
    return 0


@timer
def part_1(data: str) -> int:
    """Calculate the solution for Part 1."""
    machines = []
    for l in data.splitlines():
        ps = l.split(" ")
        goal_mask = 0
        for i, c in enumerate(ps[0][1:-1]):
            if c == "#":
                goal_mask |= 1 << i

        raw_buttons = ast.literal_eval("[" + ",".join(ps[1:-1]) + "]")

        button_masks = []
        for b in raw_buttons:
            mask = 0
            if isinstance(b, int):
                mask |= 1 << b
            else:
                for bit in b:
                    mask |= 1 << bit
            button_masks.append(mask)

        machines.append((goal_mask, button_masks))

    return sum(map(solve_machine, machines))


def solve_machine_p2(machine):
    """Solve a single machine using linear programming for Part 2."""
    goal_counters, buttons_masks = machine
    num_goals = len(goal_counters)
    num_buttons = len(buttons_masks)

    c = [1] * num_buttons

    shifts = np.arange(num_goals)
    constraint_matrix = ((np.array(buttons_masks)[:, None] >> shifts) & 1).T.astype(
        float
    )

    target_vector = np.array(goal_counters, dtype=float)

    # Fast Path: Use Least Squares for Deterministic/Overdetermined systems
    if num_buttons <= num_goals:
        try:
            x, _, rank, _ = np.linalg.lstsq(
                constraint_matrix, target_vector, rcond=None
            )
            x_rounded = np.round(x).astype(int)

            # Verify validity: Non-negative, Integer-close, Exact match
            # CRITICAL: Must be Full Rank (rank == num_buttons) to ensure uniqueness.
            if (
                rank == num_buttons
                and np.all(x_rounded >= 0)
                and np.allclose(x, x_rounded, atol=1e-5)
                and np.allclose(constraint_matrix @ x_rounded, target_vector)
            ):
                return int(np.sum(x_rounded))
        except np.linalg.LinAlgError:
            pass  # Fallback to linprog

    res = linprog(
        c,
        A_eq=constraint_matrix,
        b_eq=target_vector,
        bounds=(0, None),
        method="highs",
        integrality=True,
    )

    return round(res.fun)


@timer
def part_2(data: str) -> int:
    """Calculate the solution for Part 2."""
    machines = []
    for l in data.splitlines():
        ps = l.split(" ")

        counters_str = ps[-1][1:-1]
        goal_counters = list(map(int, counters_str.split(",")))

        raw_buttons = ast.literal_eval("[" + ",".join(ps[1:-1]) + "]")

        button_masks = []
        for b in raw_buttons:
            mask = 0
            if isinstance(b, int):
                mask |= 1 << b
            else:
                for bit in b:
                    mask |= 1 << bit
            button_masks.append(mask)

        machines.append((goal_counters, button_masks))

    return sum(map(solve_machine_p2, machines))


def main():
    """Execute the solution for both parts."""
    input_data = read_input()
    part_1(input_data)
    part_2(input_data)


if __name__ == "__main__":
    main()
