#from time import perf_counter
from time import time as perf_counter
from collections import deque


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print('Method ' + method.__name__ + ' took : ' +
              "{:2.5f}".format(perf_counter()-t) + ' sec')
        return ret
    return wrapper_method


@profiler
def part1():
    air = set()
    for l in open("input.txt"):
        air.add(tuple(map(int, l.split(","))))

    exposed = 0

    for p in air:
        for d in range(3):
            for delta in [-1, 1]:
                move = [0, 0, 0]
                move[d] = delta

                if (p[0] + move[0], p[1] + move[1], p[2] + move[2]) not in air:
                    exposed += 1

    print(exposed)


def fill(air):
    start = (0, 0, 0)

    visited = set()
    visited.add(start)

    to_visit = deque()
    to_visit.append([start])

    xs = set(p[0] for p in air)
    ys = set(p[1] for p in air)
    zs = set(p[2] for p in air)

    while to_visit:

        current_path = to_visit.popleft()
        last_p = current_path[-1]

        for d in range(3):
            for delta in [-1, 1]:
                move = [0, 0, 0]
                move[d] = delta

                new_p = (last_p[0] + move[0], last_p[1] +
                         move[1], last_p[2] + move[2])

                if new_p in air:
                    continue

                if new_p[0] < -1 or new_p[0] > max(xs) + 1:
                    continue

                if new_p[1] < -1 or new_p[1] > max(ys) + 1:
                    continue

                if new_p[2] < -1 or new_p[2] > max(zs) + 1:
                    continue

                if new_p not in current_path and new_p not in visited:
                    new_path = current_path + [new_p]
                    visited.add(new_p)
                    to_visit.append(new_path)

    return visited

@profiler
def part2():

    air = set()
    for l in open("input.txt"):
        air.add(tuple(map(int, l.split(","))))

    exposed = 0

    exposed_surfaces = fill(air)

    for p in air:
        for d in range(3):
            for delta in [-1, 1]:
                move = [0, 0, 0]
                move[d] = delta

                to_test = (p[0] + move[0], p[1] + move[1], p[2] + move[2])
                if to_test in air:
                    continue

                if to_test in exposed_surfaces:
                    exposed += 1

    print(exposed)


if __name__ == "__main__":

    part1()
    part2()
