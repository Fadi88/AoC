# pylint: disable=C0114,C0116,C0301,C0209,W1514

from time import perf_counter
from itertools import combinations
from sympy import var, Eq, solve


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print("Method " + method.__name__ + " took : " + "{:2.5f}".format(perf_counter() - t) + " sec")
        return ret

    return wrapper_method


def get_coef(p, v):
    a = v[1] / v[0]
    b = p[1] - (p[0] * v[1]) / v[0]

    return a, b


def get_intrestion(coef1, coef2):
    if coef2[0] != coef1[0]:
        return (coef2[1] - coef1[1]) / (coef1[0] - coef2[0])
    return -1


def get_time(d, d0, v):
    return (d - d0) / v


@profiler
def part1():
    particles = []

    for l in open("day24/input.txt"):
        p = l.split(" @ ")
        ps = list(map(int, p[0].split(", ")))
        vs = list(map(int, p[1].split(", ")))

        particles.append((ps, vs))

    total = 0

    lower_limit = 200000000000000
    upper_limit = 400000000000000

    for p1, p2 in combinations(particles, 2):
        pos1, v1 = p1
        pos2, v2 = p2

        c1 = get_coef(pos1, v1)
        c2 = get_coef(pos2, v2)

        x = get_intrestion(c1, c2)
        y = c1[0] * x + c1[1]

        tx1 = get_time(x, pos1[0], v1[0])
        tx2 = get_time(x, pos2[0], v2[0])

        if tx1 >= 0 and tx2 >= 0 and lower_limit <= x <= upper_limit and lower_limit <= y <= upper_limit:
            total += 1

    print(total)


@profiler
def part2():
    particles = []

    sx = var("sx")
    sy = var("sy")
    sz = var("sz")

    vx = var("vx")
    vy = var("vy")
    vz = var("vz")

    eq = []

    for l in open("day24/input.txt"):
        p = l.split(" @ ")
        ps = list(map(int, p[0].split(", ")))
        vs = list(map(int, p[1].split(", ")))

        particles.append((ps, vs))

        ts = "t{}".format(len(eq) // 3)
        exec(f'{ts} = var("{ts}")')

        eq.append(Eq(eval(f"sx + vx * {ts}"), eval(f"ps[0] + vs[0] * {ts}")))
        eq.append(Eq(eval(f"sy + vy * {ts}"), eval(f"ps[1] + vs[1] * {ts}")))
        eq.append(Eq(eval(f"sz + vz * {ts}"), eval(f"ps[2] + vs[2] * {ts}")))

        # 3 pos, 3 vs + 3 ts minimum length, otherwise same solution with more calcaution
        if len(eq) > 9:
            break

    ans = solve(eq)[0]
    print(ans[sx] + ans[sy] + ans[sz])


if __name__ == "__main__":
    part1()
    part2()
