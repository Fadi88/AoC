INF = float("inf")
EPS = 1e-9

import os
import time
import functools


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


def simplex(A, C):
    def pivot(r, s):
        k = 1 / D[r][s]
        for i in range(m + 2):
            if i == r:
                continue
            for j in range(n + 2):
                if j != s:
                    D[i][j] -= D[r][j] * D[i][s] * k
        for i in range(n + 2):
            D[r][i] *= k
        for i in range(m + 2):
            D[i][s] *= -k
        D[r][s] = k
        B[r], N[s] = N[s], B[r]

    def find(p):
        while True:
            if (
                D[m + p][
                    s := min(
                        (i for i in range(n + 1) if p or N[i] != -1),
                        key=lambda x: (D[m + p][x], N[x]),
                    )
                ]
                > -EPS
            ):
                return 1
            if (
                r := min(
                    (i for i in range(m) if D[i][s] > EPS),
                    key=lambda x: (D[x][-1] / D[x][s], B[x]),
                    default=-1,
                )
            ) == -1:
                return 0
            pivot(r, s)

    m = len(A)
    n = len(A[0]) - 1
    N = [*range(n), -1]
    B = [*range(n, n + m)]
    D = [*([*A[i], -1] for i in range(m)), C + [0] * 2, [0] * (n + 2)]
    for i in range(m):
        D[i][-2], D[i][-1] = D[i][-1], D[i][-2]
    D[-1][n] = 1
    r = min(range(m), key=lambda x: D[x][-1])
    if D[r][-1] < -EPS and (pivot(r, n) or not find(1) or D[-1][-1] < -EPS):
        return -INF, None
    for i in range(m):
        B[i] == -1 and pivot(i, min(range(n), key=lambda x: (D[i][x], N[x])))
    if find(0):
        x = [0] * n
        for i in range(m):
            if 0 <= B[i] < n:
                x[B[i]] = D[i][-1]
        return sum(C[i] * x[i] for i in range(n)), x
    else:
        return -INF, None


def f(A):
    n = len(A[0]) - 1
    bval = float("inf")
    bsol = None

    def branch(A):
        nonlocal bval, bsol

        val, x = simplex(A, [1] * n)
        if val + EPS >= bval or val == -INF:
            return

        k, v = next(
            ((i, int(e)) for i, e in enumerate(x) if abs(e - round(e)) > EPS), (-1, 0)
        )
        if k == -1:
            if val + EPS < bval:
                bval, bsol = val, [*map(round, x)]
        else:
            s = [0] * n + [v]
            s[k] = 1
            branch(A + [s])
            s = [0] * n + [~v]
            s[k] = -1
            branch(A + [s])

    branch(A)
    return round(bval)


p1 = p2 = 0
for l in open(
    os.path.join(os.path.dirname(__file__), "input.txt"), "r", encoding="utf-8"
):
    m, *p, c = l.split()
    n = len(m) - 2
    q = [*map(lambda x: eval(x[:-1] + ",)"), p)]
    c = [*map(int, c[1:-1].split(","))]

    # Part 1: bitmask BFS
    B = [-1] * (1 << n)
    B[0] = 0
    p = [*map(lambda x: sum(1 << i for i in x), q)]
    m = int(m[-2:0:-1].replace("#", "1").replace(".", "0"), 2)
    Q = [0]
    for u in Q:
        for v in p:
            if ~B[u ^ v]:
                continue
            B[u ^ v] = B[u] + 1
            Q.append(u ^ v)
    p1 += B[m]


@timer
def run_part2():
    p2 = 0
    # Re-read to ensure fair comparison
    lines = open(
        os.path.join(os.path.dirname(__file__), "input.txt"), "r", encoding="utf-8"
    ).readlines()

    for l in lines:
        m, *p, c = l.split()
        n = len(m) - 2
        q = [*map(lambda x: eval(x[:-1] + ",)"), p)]
        c = [*map(int, c[1:-1].split(","))]

        # Part 2: branch-and-bound ILP
        A = [[0] * -~len(p) for _ in range(2 * n + len(p))]
        for i in range(len(q)):
            A[~i][i] = -1
            for e in q[i]:
                A[e][i] = 1
                A[e + n][i] = -1
        for i in range(n):
            A[i][-1] = c[i]
            A[i + n][-1] = -c[i]
        p2 += f(A)
    return p2


print("Part 1:", p1)
print("Part 2:", run_part2())
