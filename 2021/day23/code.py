from os import stat
import time
from queue import PriorityQueue as pq
from collections import defaultdict
import math
from copy import deepcopy
from functools import lru_cache


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


def print_state(s):
    for l in s:
        print("".join(l))

    print()


def get_possible_states(state):
    deltas = [(-1, 0), (1, 0), (1, -1), (-1, -1), (0, -1), (0, 1), (1, 1), (-1, 1)]

    for y, l in enumerate(state):
        for x, c in enumerate(l):
            if c in ["A", "B", "C", "D"]:
                for dx, dy in deltas:
                    if state[y + dy][x + dx] == ".":
                        if (x + dx, y + dy) in [(9, 1), (7, 1), (5, 1), (3, 1)]:
                            continue
                        n_state = deepcopy(state)
                        n_state[y + dy][x + dx] = c
                        n_state[y][x] = "."

                        cost = (abs(dx) + abs(dy)) * 10 ** (ord(c) - ord("A"))

                        yield (cost, n_state)


@profiler
def part1():
    state = [list(l.rstrip()) for l in open("day23/input.txt")]

    f_str = (
        "#############\n"
        + "#...........#\n"
        + "###A#B#C#D###\n"
        + "  #A#B#C#D#\n"
        + "  #########"
    )
    f_state = [list(l) for l in f_str.split("\n")]
    visited = set()
    visit = pq()
    visit.put((0, state))

    cost = defaultdict(lambda: math.inf)
    cost[str(state)] = 0

    prev = {}

    while not visit.empty():
        c, c_state = visit.get()

        visited.add(str(c_state))

        for n_c, n_state in get_possible_states(c_state):
            if n_c < cost[str(n_state)]:
                cost[str(n_state)] = n_c + c
                prev[str(n_state)] = str(c_state)
            if str(n_state) not in visited:
                visit.put((cost[str(n_state)], n_state))


@profiler
def part2():
    state = [list(l.rstrip()) for l in open("day23/input.txt")]
    state = state[:3] + [list("  #D#C#B#A#")] + [list("  #D#B#A#C#")] + state[3:]

    f_str = (
        "#############\n"
        + "#...........#\n"
        + "###A#B#C#D###\n"
        + "  #A#B#C#D#\n"
        + "  #A#B#C#D#\n"
        + "  #A#B#C#D#\n"
        + "  #########"
    )
    f_state = [list(l) for l in f_str.split("\n")]
    visited = set()
    visit = pq()
    visit.put((0, state))

    cost = defaultdict(lambda: math.inf)
    cost[str(state)] = 0

    prev = {}

    while not visit.empty():
        c, c_state = visit.get()

        visited.add(str(c_state))

        for n_c, n_state in get_possible_states(c_state):
            if n_c < cost[str(n_state)]:
                cost[str(n_state)] = n_c + c
                prev[str(n_state)] = str(c_state)
            if str(n_state) not in visited:
                visit.put((cost[str(n_state)], n_state))

    print(cost[str(f_state)])


if __name__ == "__main__":

    part1()
    part2()
