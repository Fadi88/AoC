import time
from collections import defaultdict


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print("Method " + method.__name__ + " took : " +
              "{:2.5f}".format(time.time() - t) + " sec")
        return ret

    return wrapper_method


@profiler
def part1():

    grid = set()

    for y, l in enumerate(open("day22/input.txt").read().splitlines()):
        for x, c in enumerate(l):
            if c == "#":
                grid.add(x+y*1j)

    pos = x//2 + y//2 * 1j
    direction = -1j

    cnt = 0
    for _ in range(10000):

        if pos in grid:
            direction *= -1j ** 3
            grid.remove(pos)
        else:
            direction *= -1j ** 1
            grid.add(pos)
            cnt += 1

        pos += direction

    print(cnt)


@profiler
def part2():

    grid = {}

    for y, l in enumerate(open("day22/input.txt").read().splitlines()):
        for x, c in enumerate(l):
            if c == "#":
                grid[x+y*1j] = c

    pos = x//2 + y//2 * 1j
    direction = -1j

    cnt = 0
    for _ in range(10000000):

        if pos in grid:
            if grid[pos] == "W":
                grid[pos] = "#"
                cnt += 1
            elif grid[pos] == "#":
                grid[pos] = "F"
                direction *= -1j ** 3
                
            elif grid[pos] == "F":
                del grid[pos]
                direction *= 1j ** 2
        else:
            direction *= -1j ** 1
            grid[pos] = "W"


        pos += direction

    print(cnt)


if __name__ == "__main__":

    part1()
    part2()
