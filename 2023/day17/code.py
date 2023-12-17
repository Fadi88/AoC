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


@profiler
def part1():
    grid = [list(map(int, l.strip())) for l in open("day17/input.txt")]

    s = (0, 0)
    e = (len(grid[0]) - 1, len(grid) - 1)

    dirs = {">": (1, 0), "v": (0, 1), "^": (0, -1), "<": (-1, 0)}
    opposite = {"<": ">", ">": "<", "v": "^", "^": "v"}

    to_visit = [(grid[0][0], ">", s), (grid[0][0], "v", s)]
    to_visit = [(0, ">", s), (0, "v", s)]

    seen = set()

    while to_visit:
        cl, cd, cp = heapq.heappop(to_visit)
        if (cp, cd) in seen:
            continue
        seen.add((cp, cd))
        for d in dirs:
            n_p = (cp[0] + dirs[d][0], cp[1] + dirs[d][1])
            if (
                not 0 <= n_p[0] < len(grid[0]) # out of grid range
                or not 0 <= n_p[1] < len(grid)
                or (d == cd[-1] and len(cd) == 3) # path longer than 3 blocks
                or cd[-1] == opposite[d] # turning back
            ):
                continue
            if d == cd[-1]:
                nd = cd + d
            else:
                nd = d
            if (n_p, nd) in seen:
                continue
            if n_p == e:
                print(cl + grid[n_p[1]][n_p[0]])
                return
            heapq.heappush(to_visit, (cl + grid[n_p[1]][n_p[0]], nd, n_p))


@profiler
def part2():
    grid = [list(map(int, l.strip())) for l in open("day17/input.txt")]

    s = (0, 0)
    e = (len(grid[0]) - 1, len(grid) - 1)

    dirs = {">": (1, 0), "v": (0, 1), "^": (0, -1), "<": (-1, 0)}
    opposite = {"<": ">", ">": "<", "v": "^", "^": "v"}

    to_visit = [(grid[0][0], ">", s), (grid[0][0], "v", s)]
    to_visit = [(0, ">", s), (0, "v", s)]

    seen = set()

    while to_visit:
        cl, cd, cp = heapq.heappop(to_visit)
        if (cp, cd) in seen:
            continue
        seen.add((cp, cd))
        for d in dirs:
            n_p = (cp[0] + dirs[d][0], cp[1] + dirs[d][1])
            if (
                not 0 <= n_p[0] < len(grid[0]) # out of grid range
                or not 0 <= n_p[1] < len(grid)
                or (d == cd[-1] and len(cd) == 10) # path longer than 10 blocks
                or (d != cd[-1] and len(cd) < 4) # path shorter than 4 blocks
                or cd[-1] == opposite[d] # turning back
            ):
                continue
            if d == cd[-1]:
                nd = cd + d
            else:
                nd = d
            if (n_p, nd) in seen:
                continue
            if n_p == e:
                print(cl + grid[n_p[1]][n_p[0]])
                return
            heapq.heappush(to_visit, (cl + grid[n_p[1]][n_p[0]], nd, n_p))


if __name__ == "__main__":
    part1()
    part2()
