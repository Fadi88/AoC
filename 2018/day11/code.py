import time
import numpy as np
from scipy import signal


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


def get_cell_power(x, y, puzzle_input=8199):
    rack_id = x + 10
    power_level = rack_id * y
    power_level += puzzle_input
    power_level *= rack_id

    return (power_level // 100) % 10 - 5


@profiler
def part_1():
    highest = 0
    pt = (0, 0)
    for x in range(2, 300):
        for y in range(2, 300):
            power = sum(
                [get_cell_power(x + dx, y + dy) for dx in range(3) for dy in range(3)]
            )

            if power > highest:
                highest = power
                pt = (x, y)

    print(pt, highest)


def get_power(grid, x, y, size):
    power = 0
    for i in range(size):
        for j in range(size):
            power += grid[x + i][y + j]
    return power


@profiler
def part_2():

    grid = [[get_cell_power(x + 1, y + 1) for y in range(300)] for x in range(300)]
    grid = np.array(grid, dtype=np.float)

    max_power = 0

    for sz in range(2, 299):

        filtered = signal.convolve2d(grid, np.ones((sz, sz)), "valid")

        if np.amax(filtered) > max_power:
            max_power = np.amax(filtered)
            pt_max = np.unravel_index(np.argmax(filtered), filtered.shape)
            pt = (pt_max[0] + 1, pt_max[1] + 1, sz)
            print(pt)

    print(pt)


if __name__ == "__main__":

    part_1()
    part_2()
