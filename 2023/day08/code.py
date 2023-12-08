from time import perf_counter
import re
from math import lcm


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print("Method " + method.__name__ + " took : " + "{:2.5f}".format(perf_counter() - t) + " sec")
        return ret

    return wrapper_method


@profiler
def part1():
    input = open("day08/input.txt").read().split("\n\n")

    directions = input[0]

    maze = {}
    for l in input[1].splitlines():
        p = re.findall(r"\w{3}", l)
        maze[p[0]] = (p[1], p[2])

    state = "AAA"

    idx = 0
    while state != "ZZZ":
        match directions[idx % len(directions)]:
            case "R":
                state = maze[state][1]
            case "L":
                state = maze[state][0]

        idx += 1
    print(idx)


def get_distance(maze, directions, start):
    state = start
    idx = 0

    while state[2] != "Z":
        match directions[idx % len(directions)]:
            case "R":
                state = maze[state][1]
            case "L":
                state = maze[state][0]

        idx += 1

    return idx


@profiler
def part2():
    input = open("day08/input.txt").read().split("\n\n")

    directions = input[0]

    maze = {}

    As = []

    for l in input[1].splitlines():
        p = re.findall(r"\w{3}", l)
        maze[p[0]] = (p[1], p[2])
        if p[0][2] == "A":
            As.append(p[0])

    dist = [get_distance(maze, directions, a) for a in As]

    print(lcm(*dist))


if __name__ == "__main__":
    part1()
    part2()
