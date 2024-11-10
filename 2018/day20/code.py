# pylint: disable=C0114, C0116, C0209

import time
import heapq

DEPTH = 10647
TARGET = (7, 770)

# DEPTH = 510
# TARGET = (10, 10)


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
def part_1():
    inp = open("day20/input.txt", "r").read()

    c_pos = 0
    deltas = {"E": 1, "W": -1, "N": 1j, "S": -1j}

    distance = {c_pos: 0}
    branches = []

    for c in inp:
        if c in deltas:
            n_pos = c_pos + deltas[c]
            if n_pos not in distance:
                distance[n_pos] = distance[c_pos] + 1
            else:
                distance[n_pos] = min(distance[c_pos] + 1, distance[n_pos])
            c_pos = n_pos
        elif c == "(":
            branches.append(c_pos)
        elif c == ")":
            c_pos = branches.pop()
        elif c == "|":
            c_pos = branches[-1]

    print(max(distance.values()))


@profiler
def part_2():
    inp = open("day20/input.txt", "r").read()

    c_pos = 0
    deltas = {"E": 1, "W": -1, "N": 1j, "S": -1j}

    distance = {c_pos: 0}
    branches = []

    for c in inp:
        if c in deltas:
            n_pos = c_pos + deltas[c]
            if n_pos not in distance:
                distance[n_pos] = distance[c_pos] + 1
            else:
                distance[n_pos] = min(distance[c_pos] + 1, distance[n_pos])
            c_pos = n_pos
        elif c == "(":
            branches.append(c_pos)
        elif c == ")":
            c_pos = branches.pop()
        elif c == "|":
            c_pos = branches[-1]

    print(len(list(filter(lambda x: x >= 1000, distance.values()))))


if __name__ == "__main__":
    part_1()
    part_2()
