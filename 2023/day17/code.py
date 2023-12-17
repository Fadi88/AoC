# pylint: disable=C0114,C0116,C0301,C0209,W1514,C0206

from time import perf_counter
import heapq


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print("Method " + method.__name__ + " took : " + "{:2.5f}".format(perf_counter() - t) + " sec")
        return ret

    return wrapper_method


def get_min(grid, min_l=1, max_l=3):
    s = (0, 0)
    e = (len(grid[0]) - 1, len(grid) - 1)

    max_x = len(grid[0])
    max_y = len(grid)

    dirs = {">": (1, 0), "v": (0, 1), "^": (0, -1), "<": (-1, 0)}
    opposite = {"<": ">", ">": "<", "v": "^", "^": "v"}

    to_visit = [(0, ">", s), (0, "v", s)]

    seen = set()

    while to_visit:
        cl, cd, cp = heapq.heappop(to_visit)
        if (cp, cd) in seen:
            continue

        seen.add((cp, cd))
        path_len = len(cd)

        for d in dirs:
            n_p = (cp[0] + dirs[d][0], cp[1] + dirs[d][1])
            if (
                not 0 <= n_p[0] < max_x  # out of grid range
                or not 0 <= n_p[1] < max_y
                or (d == cd[-1] and path_len == max_l)  # path longer
                or (d != cd[-1] and path_len < min_l)  # path shorter
                or cd[-1] == opposite[d]  # turning back
            ):
                continue
            if d == cd[-1]:
                nd = cd + d
            else:
                nd = d
            if (n_p, nd) in seen:
                continue
            if n_p == e and len(nd) >= min_l:
                return cl + grid[n_p[1]][n_p[0]]
            heapq.heappush(to_visit, (cl + grid[n_p[1]][n_p[0]], nd, n_p))


@profiler
def part1():
    grid = [list(map(int, l.strip())) for l in open("day17/input.txt")]

    print(get_min(grid))


@profiler
def part2():
    grid = [list(map(int, l.strip())) for l in open("day17/input.txt")]

    print(get_min(grid, 4, 10))


if __name__ == "__main__":
    part1()
    part2()
