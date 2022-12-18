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


def is_exposed(air, p):
    target = (0, 0, 0)

    visited = set()
    visited.add(p)

    to_visit = deque()
    to_visit.append([p])

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

                if new_p[0] < min(xs) - 1 or new_p[0] > max(xs) + 1:
                    continue

                if new_p[1] < min(ys) - 1  or new_p[1] > max(ys) + 1:
                    continue

                if new_p[2] < min(zs) - 1  or new_p[2] > max(zs) + 1:
                    continue

                if new_p not in current_path and new_p not in visited and new_p not in air:
                    new_path = current_path + [new_p]
                    if new_p == target:
                        return True,new_path
                    visited.add(new_p)
                    to_visit.append(new_path)

    return False,None


@profiler
def part2():
    air = set()
    for l in open("input.txt"):
        air.add(tuple(map(int, l.split(","))))

    exposed = 0

    cache = {}
    for p in air:
        for d in range(3):
            for delta in [-1, 1]:
                move = [0, 0, 0]
                move[d] = delta

                to_test = (p[0] + move[0], p[1] + move[1], p[2] + move[2])
                if to_test in air:
                    continue

                if to_test not in cache:
                    state,path = is_exposed(air, to_test)
                    if state:
                        for np in path:
                            cache[np] = True
                    else:
                        cache[to_test] = False

                if cache[to_test]:
                    exposed += 1

    print(exposed)


if __name__ == "__main__":

    # part1()
    part2()
