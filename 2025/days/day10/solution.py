"""Advent of Code Day 10 Solution"""

import os
import time
import functools
import ast
from collections import deque
import numpy as np
from scipy.optimize import linprog

TOL = 1e-5


def timer(func):
    """Timing decorator."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        t0 = time.perf_counter()
        res = func(*args, **kwargs)
        dt = time.perf_counter() - t0
        print(f"[{func.__name__}] Time: {dt*1000:.4f} ms")
        return res

    return wrapper


def read_input():
    """Read input file."""
    with open(
        os.path.join(os.path.dirname(__file__), "input.txt"), "r", encoding="utf-8"
    ) as f:
        return f.read().strip()


def parse_input(data):
    """Parse input data into machines."""
    machines = []
    for line in data.splitlines():
        ps = line.split(" ")
        goal_mask = 0
        for i, c in enumerate(ps[0][1:-1]):
            if c == "#":
                goal_mask |= 1 << i

        goal_counters = list(map(int, ps[-1][1:-1].split(",")))

        raw = ast.literal_eval("[" + ",".join(ps[1:-1]) + "]")
        button_masks = []
        for b in raw:
            m = 0
            if isinstance(b, int):
                m |= 1 << b
            else:
                for bit in b:
                    m |= 1 << bit
            button_masks.append(m)
        machines.append((goal_mask, goal_counters, button_masks))
    return machines


def solve_bfs(goal, buttons):
    """Solve using BFS (Part 1)."""
    q = deque([(0, 0)])
    vis = {0}
    while q:
        curr, steps = q.popleft()
        if curr == goal:
            return steps
        for b in buttons:
            nxt = curr ^ b
            if nxt not in vis:
                vis.add(nxt)
                q.append((nxt, steps + 1))
    return 0


def solve_p2(goal_vals, buttons):
    """Solve using Hybrid Linear Solver (Part 2)."""
    num_rows, num_cols = len(goal_vals), len(buttons)
    shifts = np.arange(num_rows)
    # A[i, j] = 1 if button j affects bit i
    matrix = ((np.array(buttons)[:, None] >> shifts) & 1).T.astype(float)
    target = np.array(goal_vals, dtype=float)

    if num_cols <= num_rows:
        try:
            x, _, rank, _ = np.linalg.lstsq(matrix, target, rcond=None)
            xr = np.round(x).astype(int)
            if (
                rank == num_cols
                and np.all(xr >= 0)
                and np.allclose(x, xr, atol=TOL)
                and np.allclose(matrix @ xr, target)
            ):
                return int(np.sum(xr))
        except np.linalg.LinAlgError:
            pass

    res = linprog(
        [1] * num_cols,
        A_eq=matrix,
        b_eq=target,
        bounds=(0, None),
        method="highs",
        integrality=True,
    )
    return round(res.fun)


@timer
def part_1(machines):
    """Run Part 1."""
    return sum(solve_bfs(m[0], m[2]) for m in machines)


@timer
def part_2(machines):
    """Run Part 2."""
    return sum(solve_p2(m[1], m[2]) for m in machines)


def main():
    """Main execution."""
    data = parse_input(read_input())
    print(f"[part_1] Result: {part_1(data)}")
    print(f"[part_2] Result: {part_2(data)}")


if __name__ == "__main__":
    main()
