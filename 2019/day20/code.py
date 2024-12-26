# pylint: disable=C0114,C0116,C0301,C0209,W1514,C0414,E0001,R0914,C0206,R1702

from typing import Any
import os
from time import perf_counter_ns

input_file = os.path.join(os.path.dirname(__file__), "day20_input.txt")
# input_file = os.path.join(os.path.dirname(__file__), "test.txt")


def profiler(method):

    def wrapper_method(*args: Any, **kwargs: Any) -> Any:
        start_time = perf_counter_ns()
        ret = method(*args, **kwargs)
        stop_time = perf_counter_ns() - start_time
        time_len = min(9, ((len(str(stop_time))-1)//3)*3)
        time_conversion = {9: 'seconds', 6: 'milliseconds',
                           3: 'microseconds', 0: 'nanoseconds'}
        print(f"Method {method.__name__} took : {
              stop_time / (10**time_len)} {time_conversion[time_len]}")
        return ret

    return wrapper_method


def parse():
    free_spaces = set()
    portals_raw = {}
    x, y = -1, -1
    with open(input_file) as f:
        for y, l in enumerate(f.readlines()):
            max_y = y + 1
            for x, c in enumerate(l):
                if c == ".":
                    free_spaces.add((x, y))
                elif c.isalpha():
                    portals_raw[(x, y)] = c
            max_x = x + 1

    portal_mapped = {}
    outer_portals = {}
    for p in free_spaces:
        for d in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if (p[0] + d[0], p[1] + d[1]) in portals_raw:
                name = portals_raw[(p[0] + d[0], p[1] + d[1])] + \
                    portals_raw[(p[0] + 2*d[0], p[1] + 2*d[1])]
                portal_mapped[p] = "".join(sorted(name))
                if portal_mapped[p] == "AA":
                    start = p
                outer_portals[p] = p[0] in [
                    2, max_x - 3] or p[1] in [2, max_y - 3]
                break

    return start, portal_mapped, outer_portals, free_spaces


@profiler
def part_1():

    start, portal_mapped, _, free_spaces = parse()

    seen = set()

    to_visit = [(start, 0)]
    while to_visit:
        p, steps = to_visit.pop(0)
        if p in seen:
            continue
        seen.add(p)
        for d in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            np = (p[0] + d[0], p[1] + d[1])
            if np in portal_mapped and np not in seen:
                name = portal_mapped[np]
                if name == "ZZ":
                    print(steps + 1)
                    return
                for jp in portal_mapped:
                    if portal_mapped[jp] == name and jp != np:
                        to_visit.append((jp, steps + 2))
                        break
            elif np in free_spaces and np not in seen:
                to_visit.append((np, steps + 1))


@ profiler
def part_2():

    start, portal_mapped, outer_portals, free_spaces = parse()

    seen = set()

    to_visit = [(start, 0, 0)]
    while to_visit:
        p, steps, level = to_visit.pop(0)
        if (p, level) in seen:
            continue
        seen.add((p, level))
        for d in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            np = (p[0] + d[0], p[1] + d[1])
            if np in portal_mapped and np not in seen:
                name = portal_mapped[np]
                if level == 0:
                    if name == "ZZ":
                        print(steps + 1)
                        return
                    if outer_portals[np]:
                        continue
                else:
                    if name in ["AA", "ZZ"]:
                        continue
                for jp in portal_mapped:
                    if portal_mapped[jp] == name and jp != np:
                        if level == 0 and portal_mapped[jp] in ["AA", "ZZ"]:
                            continue
                        dl = 1 if outer_portals[jp] else -1
                        to_visit.append((jp, steps + 2, level + dl))
                        break
            elif np in free_spaces:
                to_visit.append((np, steps + 1, level))


if __name__ == "__main__":
    part_1()
    part_2()
