# pylint: disable=C0114,C0116,C0301,C0209,W1514,C0414

from time import perf_counter_ns
from typing import Any
import os

input_file = os.path.join(os.path.dirname(__file__), "input.txt")
# input_file = os.path.join(os.path.dirname(__file__), "test.txt")


def profiler(method):

    def wrapper_method(*args: Any, **kwargs: Any) -> Any:
        start_time = perf_counter_ns()
        ret = method(*args, **kwargs)
        duration = perf_counter_ns() - start_time
        time_len = min(9, ((len(str(duration))-1)//3)*3)
        time_conversion = {9: 'seconds', 6: 'milliseconds',
                           3: 'microseconds', 0: 'nanoseconds'}
        print(f"Method {method.__name__} took : {
              duration / (10**time_len)} {time_conversion[time_len]}")
        return ret

    return wrapper_method


def free_space(robot, d, walls, boxes):
    dx, dy = d[0], d[1]

    cx, cy = robot[0] + dx, robot[1] + dy

    while True:
        if (cx, cy) in walls:
            return False, (-1, -1)
        if (cx, cy) in boxes:
            cx, cy = cx + dx, cy + dy
        else:
            return True, (cx, cy)


@profiler
def part_1():
    with open(input_file) as f:
        g, moves = f.read().split("\n\n")

    robot = (-1, -1)
    boxes = set()
    walls = set()

    deltas = {
        "^": (0, -1),
        ">": (1, 0),
        "v": (0, 1),
        "<": (-1, 0)
    }

    for y, l in enumerate(g.split("\n")):
        for x, h in enumerate(l):
            if h == "O":
                boxes.add((x, y))
            elif h == "#":
                walls.add((x, y))
            elif h == "@":
                robot = (x, y)

    moves = moves.replace("\n", "")
    for m in moves:
        dx, dy = deltas[m]
        nx, ny = robot[0] + dx, robot[1] + dy

        if (nx, ny) not in walls:
            if (nx, ny) not in boxes:
                robot = (nx, ny)
            else:
                is_free, next_free = free_space(robot, (dx, dy), walls, boxes)
                if is_free:
                    to_remove = set()
                    to_add = set()

                    for b in boxes:
                        xs = [robot[0], next_free[0]]
                        ys = [robot[1], next_free[1]]
                        if min(xs) <= b[0] <= max(xs) and min(ys) <= b[1] <= max(ys):
                            to_remove.add(b)
                            to_add.add((b[0] + dx, b[1] + dy))
                    boxes -= to_remove
                    boxes |= to_add

                    robot = (robot[0]+dx, robot[1]+dy)
    print(sum(b[0] + 100*b[1] for b in boxes))


def print_map(robot, boxes, walls):
    xs = set(w[0] for w in walls)
    ys = set(w[1] for w in walls)

    grid = [['.' for _ in range(max(xs)+1)] for _ in range(max(ys)+1)]

    for w in walls:
        grid[w[1]][w[0]] = '#'
    for b1, b2 in boxes:
        grid[b1[1]][b1[0]] = '['
        grid[b2[1]][b2[0]] = ']'

    grid[robot[1]][robot[0]] = '@'

    for y, l in enumerate(grid):
        print(f"{y:02d}", end=" ")
        print(''.join(l))


def is_free_x(robot, dx, walls, boxes):

    wx = set(w[0] for w in walls if w[1] == robot[1])
    bx = set(b[0] for bs in boxes for b in bs if b[1] == robot[1])

    cx = robot[0] + dx
    while True:
        if cx in wx:
            return False, -1
        if cx in bx:
            cx += dx
        else:
            return True, cx


def is_free_y(robot, dy, walls, boxes):
    to_move = set((b1, b2) for b1, b2 in boxes if robot[0] in [
                  b1[0], b2[0]] and robot[1] + dy == b1[1])

    top = list(to_move)
    # get the top of the stack to move
    while True:
        new_top = []
        added = False
        for b1, b2 in top:
            xs = {x: (nb1, nb2) for nb1, nb2 in boxes for x in (
                nb1[0], nb2[0]) if nb1[1] == b1[1] + dy}
            to_add = set(xs[x] for x in [b1[0], b2[0]] if x in xs)
            if len(to_add) > 0:
                new_top.extend(to_add)
                to_move |= to_add
                added = True
            else:
                new_top.append((b1, b2))

        top = new_top

        if not added:
            break

    for b1, b2 in to_move:
        if (b1[0], b1[1]+dy) in walls or (b2[0], b2[1]+dy) in walls:
            return False, None

    return True, to_move


@profiler
def part_2():
    with open(input_file) as f:
        g, moves = f.read().split("\n\n")

    robot = (-1, -1)
    boxes = set()
    walls = set()

    deltas = {
        "^": (0, -1),
        ">": (1, 0),
        "v": (0, 1),
        "<": (-1, 0)
    }

    boxes = set()
    walls = set()
    robot = (-1, -1)

    for y, l in enumerate(g.split("\n")):
        for x, h in enumerate(l):
            if h == "O":
                boxes.add(((2*x, y), (2*x+1, y)))
            elif h == "#":
                walls.add(((2*x, y)))
                walls.add(((2*x + 1, y)))
            elif h == "@":
                robot = (2*x, y)

    moves = moves.replace("\n", "")

    for m in moves:
        dx, dy = deltas[m]
        if (robot[0]+dx, robot[1]+dy) in walls:
            continue
        if dy == 0:
            is_free, next_free = is_free_x(robot, dx, walls, boxes)
            if is_free:
                min_x = min(next_free, robot[0])
                max_x = max(next_free, robot[0])
                to_move = set(
                    (b1, b2)for b1, b2 in boxes if b1[1] == robot[1] and min_x <= b1[0] <= max_x)
                boxes -= to_move
                boxes |= set(((b1[0]+dx, b1[1]), (b2[0]+dx, b2[1]))
                             for b1, b2 in to_move)
                robot = (robot[0]+dx, robot[1])
        else:
            up = set((b1, b2) for b1, b2 in boxes if robot[0] in [
                     b1[0], b2[0]] and robot[1] + dy == b1[1])
            if len(up) == 0:
                robot = (robot[0], robot[1]+dy)
            else:
                is_free, to_move = is_free_y(robot, dy, walls, boxes)

                if is_free:
                    boxes -= to_move
                    boxes |= set(((b1[0], b1[1]+dy), (b2[0], b2[1]+dy))
                                 for b1, b2 in to_move)
                    robot = (robot[0], robot[1] + dy)

    print(sum(b[0] + 100*b[1] for b, _ in boxes))


if __name__ == "__main__":
    part_1()
    part_2()
