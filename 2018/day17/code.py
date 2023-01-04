from collections import deque
import time
import re


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print("Method " + method.__name__ + " took : " +
              "{:2.5f}".format(time.time() - t) + " sec")
        return ret

    return wrapper_method


def print_grid(grid):
    xs = [int(p.real) for p in grid.keys()]
    ys = [int(p.imag) for p in grid.keys()]

    for y in range(min(ys), max(ys) + 1):
        for x in range(min(xs), max(xs) + 1):
            if x + y * 1j in grid:
                print(grid[x+y*1j], end="")
            else:
                print(".", end="")
        print()


def fill_grid(grid):

    max_y = max(p.imag for p in grid)

    to_visit = deque([500])

    while to_visit:
        pos = to_visit.popleft()

        if pos in grid and grid[pos] == "~":
            to_visit.append(pos-1j)
            continue

        while pos + 1j not in grid or grid[pos + 1j] not in ["#", "~"]:
            pos += 1j
            grid[pos] = "|"

            if pos.imag == max_y:
                break

        if pos.imag == max_y:
            continue

        r_pos = pos

        while (r_pos + 1 not in grid or grid[r_pos + 1] == "|") and r_pos + 1 + 1j in grid and grid[r_pos + 1 + 1j] in ["#", "~"]:
            r_pos += 1

        l_pos = pos

        while (l_pos - 1 not in grid or grid[l_pos - 1] == "|") and l_pos - 1 + 1j in grid and grid[l_pos - 1 + 1j] in ["#", "~"]:
            l_pos -= 1

        if l_pos - 1 in grid and grid[l_pos - 1] == "#" and r_pos + 1 in grid and grid[r_pos + 1] == "#" and pos.imag > 0:
            to_visit.append(pos - 1j)

            for x in range(int(l_pos.real), int(r_pos.real) + 1):
                grid[x + pos.imag * 1j] = "~"
        else:
            for x in range(int(l_pos.real), int(r_pos.real) + 1):
                grid[x + pos.imag * 1j] = "|"
            if l_pos - 1 not in grid:
                to_visit.append(l_pos - 1)
                grid[l_pos - 1] = "|"
            if r_pos + 1 not in grid:
                to_visit.append(r_pos + 1)
                grid[r_pos + 1] = "|"


@profiler
def part_1():
    grid = {}

    for l in open("day17/input.txt"):
        p = re.findall(r"\d+", l)
        if l.startswith("x"):
            for y in range(int(p[1]), int(p[2]) + 1):
                grid[int(p[0]) + y * 1j] = "#"
        else:
            for x in range(int(p[1]), int(p[2]) + 1):
                grid[x + int(p[0])*1j] = "#"

    min_y = min(p.imag for p in grid)
    max_y = max(p.imag for p in grid)

    fill_grid(grid)

    vals = list(grid[p] for p in grid if min_y <= p.imag <= max_y)
    print(vals.count("|") + vals.count("~"))
    ys = set(list(p.real for p in grid))


@profiler
def part_2():
    grid = {}

    for l in open("day17/input.txt"):
        p = re.findall(r"\d+", l)
        if l.startswith("x"):
            for y in range(int(p[1]), int(p[2]) + 1):
                grid[int(p[0]) + y * 1j] = "#"
        else:
            for x in range(int(p[1]), int(p[2]) + 1):
                grid[x + int(p[0])*1j] = "#"

    fill_grid(grid)

    print(list(grid.values()).count("~"))


if __name__ == "__main__":

    part_1()
    part_2()
