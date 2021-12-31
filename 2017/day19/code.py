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

    # CCW starting down
    directions = [(0, 1), (-1, 0), (0, -1), (1, 0)]
    dir_i = 0

    path = []
    collected = ""

    while len(collected) < len(chars):
        cx, cy = cp
        if grid[cy][cx] in ["|", "-"] or grid[cy][cx] in chars:
            path.append(cp)
            if grid[cy][cx] in chars:
                collected += grid[cy][cx]
            dx, dy = directions[dir_i]
            cp = (cx + dx, cy + dy)
        elif grid[cy][cx] == "+":
            dx_90, dy_90 = directions[(dir_i + 1) % len(directions)]
            dx_270, dy_270 = directions[(dir_i + 3) % len(directions)]
            if grid[cy + dy_90][cx + dx_90] in ["|", "-"]:
                dir_i = (dir_i + 1) % len(directions)
                dx, dy = directions[dir_i]
                cp = (cx + dx, cy + dy)
                path.append(cp)
            elif grid[cy + dy_270][cx + dx_270] in ["|", "-"]:
                dir_i = (dir_i + 3) % len(directions)
                dx, dy = directions[dir_i]
                cp = (cx + dx, cy + dy)
                path.append(cp)
            else:
                assert False

        else:
            assert False

    print("part 1 : ", collected)
    print("part 2 : ", len(path))


if __name__ == "__main__":

    part1()
