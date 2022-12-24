import cProfile
from collections import deque
from time import time as perf_counter
#from math import lcm


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print('Method ' + method.__name__ + ' took : ' +
              "{:2.5f}".format(perf_counter()-t) + ' sec')
        return ret
    return wrapper_method


class blizzard:
    def __init__(self, direction, pos):
        self.direction = direction
        self.pos = pos

    def __str__(self):
        return str(self.pos) + self.direction + " "


def cycle_grid(grid, max_x, max_y):
    new_grid = set()
    for b in grid:
        x, y = b.pos
        if b.direction == ">":
            x += 1
            if x >= max_x:
                x = 1
        elif b.direction == "<":
            x -= 1
            if x == 0:
                x = max_x - 1
        elif b.direction == "^":
            y -= 1
            if y == 0:
                y = max_y - 1
        elif b.direction == "v":
            y += 1
            if y >= max_y:
                y = 1

        new_grid.add(blizzard(b.direction, (x, y)))

    return new_grid


@profiler
def part1():
    grid = set()

    for y, l in enumerate(open("input.txt").read().splitlines()):
        for x, c in enumerate(l):
            if c in ["<", ">", "^", "v"]:
                grid.add(blizzard(c, (x, y)))

    max_x = x
    max_y = y

    target = (x-1, y)

    start = (1, 0)

    history = {0: grid}
    occupied = {0: set(b.pos for b in history[0])}

    to_visit = deque([(start, 0)])
    deltas = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    seen = set()

    while to_visit:
        current_pos, current_step = to_visit.popleft()

        if (current_pos, current_step) in seen:
            continue

        seen.add((current_pos, current_step))

        if (current_step + 1) not in history:
            history[current_step +
                    1] = cycle_grid(history[current_step], max_x, max_y)
            occupied[current_step +
                     1] = set(b.pos for b in history[current_step + 1])

        if current_pos not in occupied[current_step + 1]:
            # wait for one minute if the place is blizzard free the next step
            to_visit.append((current_pos, current_step + 1))

        for d in deltas:
            nx, ny = current_pos[0] + d[0], current_pos[1] + d[1]

            if (nx, ny) == target:
                print(current_step+1)
                return

            if 0 < nx < max_x and 0 < ny < max_y:
                if (nx, ny) not in occupied[current_step + 1]:
                    to_visit.append(((nx, ny), current_step + 1))


@profiler
def part2():
    grid = set()

    for y, l in enumerate(open("input.txt").read().splitlines()):
        for x, c in enumerate(l):
            if c in ["<", ">", "^", "v"]:
                grid.add(blizzard(c, (x, y)))

    max_x = x
    max_y = y

    # cycle = lcm(max_x-1,max_y-1) # not in pypy
    cycle = 700

    target = (x-1, y)

    start = (1, 0)

    history = {0: grid}
    occupied = {0: set(b.pos for b in history[0])}

    to_visit = deque([(start, 0)])
    deltas = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    seen = set()

    times = []

    while to_visit:
        current_pos, current_step = to_visit.popleft()

        if (current_pos, current_step) in seen:
            continue

        seen.add((current_pos, current_step))

        if (current_step + 1) % cycle not in history:
            history[(current_step + 1) %
                    cycle] = cycle_grid(history[current_step % cycle], max_x, max_y)
            occupied[(current_step + 1) %
                     cycle] = set(b.pos for b in history[(current_step + 1) % cycle])

        if current_pos not in occupied[(current_step + 1) % cycle]:
            # wait for one minute if the place is blizzard free the next step
            to_visit.append((current_pos, current_step + 1))

        for d in deltas:
            nx, ny = current_pos[0] + d[0], current_pos[1] + d[1]

            if (nx, ny) == target:
                if len(times) == 0:
                    times.append(current_step+1)
                    to_visit.clear()
                    to_visit.append((target, current_step+1))
                    break
                if len(times) == 2:
                    print(current_step+1)
                    return

            if (nx, ny) == start and len(times) == 1:
                times.append(current_step+1)
                to_visit.clear()
                to_visit.append((start, current_step+1))
                break

            if 0 < nx < max_x and 0 < ny < max_y:
                if (nx, ny) not in occupied[(current_step + 1) % cycle]:
                    to_visit.append(((nx, ny), current_step + 1))


if __name__ == "__main__":

    part1()
    part2()
