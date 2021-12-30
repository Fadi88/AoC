import time


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print(
            "Method "
            + method.__name__
            + " took : "
            + "{:2.5f}".format(time.time() - t)
            + " sec"
        )
        return ret

    return wrapper_method


@profiler
def part1():

    grid = [list(l) for l in open("day19/input.txt").read().split("\n")]

    chars = set()

    for l in grid:
        chars = chars.union(set(l))

    chars -= {" ", "-", "|", "+"}

    cp = (grid[0].index("|"), 0)

    deltas = {
        "|": [(0, 1), (0, -1)],
        "-": [(1, 0), (-1, 0)],
        "+": [(1, 0), (-1, 0), (0, 1), (0, -1)],
    }

    path = set()
    path.add(cp)

    collected = ""
    cnt = 1

    while len(collected) < len(chars):
        cx, cy = cp
        cnt += 1
        for dx, dy in deltas[grid[cy][cx]]:
            if 0 <= cx + dx < len(grid[0]) and 0 <= cy + dy < len(grid):
                if grid[cy][cx] == "+":
                    if (
                        dx != 0
                        and grid[cy + dy][cx + dx] == "-"
                        and (cx + dx, cy + dy) not in path
                    ):
                        cp = (cx + dx, cy + dy)
                        path.add((cx + dx, cy + dy))
                        break
                    elif (
                        dy != 0
                        and grid[cy + dy][cx + dx] == "|"
                        and (cx + dx, cy + dy) not in path
                    ):
                        cp = (cx + dx, cy + dy)
                        path.add((cx + dx, cy + dy))
                        break
                else:
                    if (
                        grid[cy + dy][cx + dx] == grid[cy][cx]
                        or grid[cy + dy][cx + dx] == "+"
                    ) and (cx + dx, cy + dy) not in path:
                        cp = (cx + dx, cy + dy)
                        path.add((cx + dx, cy + dy))

                    elif grid[cy + dy][cx + dx] in chars:
                        collected += grid[cy + dy][cx + dx]
                        grid[cy + dy][cx + dx] = grid[cy][cx]
                        cp = (cx + dx, cy + dy)
                        path.add((cx + dx, cy + dy))

                    else:
                        if 0 <= cx + 2 * dx < len(grid[0]) and 0 <= cy + 2 * dy < len(
                            grid
                        ):
                            if (
                                grid[cy + 2 * dy][cx + 2 * dx] == grid[cy][cx]
                                or grid[cy + 2 * dy][cx + 2 * dx] == "+"
                                or grid[cy + 2 * dy][cx + 2 * dx] in chars
                            ) and (cx + 2 * dx, cy + 2 * dy) not in path:
                                cp = (cx + 2 * dx, cy + 2 * dy)
                                path.add((cx + 2 * dx, cy + 2 * dy))
                                cnt += 1
                            if grid[cy + 2 * dy][cx + 2 * dx] in chars:
                                collected += grid[cy + 2 * dy][cx + 2 * dx]
                                grid[cy + 2 * dy][cx + 2 * dx] = grid[cy][cx]

    print("part 1 : ", collected)
    print("part 2 : ", cnt)


if __name__ == "__main__":

    part1()
