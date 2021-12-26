import time
import math
from queue import PriorityQueue as pq
from copy import deepcopy
from collections import defaultdict


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


def get_possible_states(state):
    ret = []

    room_size = len(state) - 2

    rooms_char = {3: "A", 5: "B", 7: "C", 9: "D"}
    chars_pos = {"A": 3, "B": 5, "C": 7, "D": 9}
    cost = {"A": 1, "B": 10, "C": 100, "D": 1000}
    hallway_spot = [1, 2, 4, 6, 8, 10, 11]

    for x in hallway_spot:
        if state[1][x] in "ABCD":
            x_target = chars_pos[state[1][x]]
            if all(
                [
                    state[y][x_target] == "." or state[y][x_target] == state[1][x]
                    for y in range(2, 2 + room_size - 1)
                ]
            ):

                x_range = sorted([x, x_target])
                if all(
                    [
                        state[1][n_x] == "." or state[1][n_x] == state[1][x]
                        for n_x in range(x_range[0], x_range[1] + 1)
                    ]
                ):
                    y_target = max(
                        [
                            n_y
                            for n_y in range(2, 2 + room_size - 1)
                            if state[n_y][x_target] == "."
                        ]
                    )
                    n_state = deepcopy(state)
                    n_state[y_target][x_target] = state[1][x]
                    n_state[1][x] = "."
                    yield (
                        (x_range[1] - x_range[0] + y_target - 1) * cost[state[1][x]],
                        n_state,
                    )

    # create state where we push amphipod out of the rooms
    for x in [3, 5, 7, 9]:
        if all(
            [
                state[y][x] == "." or state[y][x] == rooms_char[x]
                for y in range(2, 2 + room_size - 1)
            ]
        ):
            continue

        for y in range(2, 2 + room_size - 1):
            if state[y][x] != ".":
                if all(
                    [
                        state[n_y][x] == rooms_char[x]
                        for n_y in range(y, 2 + room_size - 1)
                    ]
                ):
                    break
                for n_x in list(filter(lambda c: c < x, hallway_spot))[::-1]:
                    if state[1][n_x] == ".":
                        n_state = deepcopy(state)
                        n_state[1][n_x] = state[y][x]
                        n_state[y][x] = "."
                        yield ((y - 1 + x - n_x) * cost[state[y][x]], n_state)
                    else:
                        break
                for n_x in list(filter(lambda c: c > x, hallway_spot)):
                    if state[1][n_x] == ".":
                        n_state = deepcopy(state)
                        n_state[1][n_x] = state[y][x]
                        n_state[y][x] = "."
                        yield ((y - 1 + n_x - x) * cost[state[y][x]], n_state)
                    else:
                        break
                break


def print_state(state):
    for l in state:
        print("".join(l))
    print()

def get_state_string(state):
    st = "".join(state[1][1:-1])
    for x in [3, 5, 7, 9]:
        for y in range(2,len(state) - 1):
            st += state[y][x]

    return st

@profiler
def part1():
    state = [list(l.rstrip()) for l in open("day23/input.txt")]

    f_str = "...........AABBCCDD"

    visit = pq()
    visit.put((0, state))

    cost = defaultdict(lambda : math.inf)

    while not visit.empty():
        c_c, c_s = visit.get()

        if get_state_string(c_s) == f_str:
            break
        for n_c, n_s in get_possible_states(c_s):
            if cost[get_state_string(n_s)] > n_c + c_c:
                cost[get_state_string(n_s)] = n_c + c_c
                visit.put((c_c + n_c, n_s))

    print(cost[f_str])


@profiler
def part2():
    state = [list(l.rstrip()) for l in open("day23/input.txt")]

    state = state[:3] + [list("  #D#C#B#A#")] + [list("  #D#B#A#C#")] + state[-2:]
    
    f_str = "...........AAAABBBBCCCCDDDD"

    visit = pq()
    visit.put((0, state))

    cost = defaultdict(lambda : math.inf)

    while not visit.empty():
        c_c, c_s = visit.get()

        if get_state_string(c_s) == f_str:
            break
        for n_c, n_s in get_possible_states(c_s):
            if cost[get_state_string(n_s)] > n_c + c_c:
                cost[get_state_string(n_s)] = n_c + c_c
                visit.put((c_c + n_c, n_s))

    print(cost[f_str])


if __name__ == "__main__":

    part1()
    part2()
