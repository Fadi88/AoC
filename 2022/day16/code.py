#from time import perf_counter
from collections import defaultdict, deque
from time import time as perf_counter


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print('Method ' + method.__name__ + ' took : ' +
              "{:2.5f}".format(perf_counter()-t) + ' sec')
        return ret
    return wrapper_method


def explore(v, key_valves, grid):
    ret = {}

    for target_v in key_valves:
        if v == target_v:
            continue

        to_visit = deque()
        to_visit.append([v])

        while to_visit:
            current_path = to_visit.popleft()

            if current_path[-1] == target_v:
                ret[target_v] = len(current_path) - 1
                break

            for n_v in grid[current_path[-1]]:
                if n_v in current_path:
                    continue
                new_path = [] + current_path + [n_v]

                to_visit.append(new_path)

    return ret


def get_time_elapsed(grid, path):
    time_elapsed = 0

    for i in range(1, len(path)):
        time_elapsed += grid[path[i-1]][path[i]] + 1

    return time_elapsed


def get_pressure(grid, flow_rate, path, time_remaining=30):
    total_pressure = 0

    for i in range(1, len(path)):
        if time_remaining > grid[path[i-1]][path[i]] + 1:
            time_remaining -= grid[path[i-1]][path[i]] + 1
            total_pressure += flow_rate[path[i]] * time_remaining
        else:
            break

    return total_pressure


@profiler
def part1():
    grid = {}
    flow_rate = {}

    for l in open("input.txt").read().splitlines():
        ps = l.replace(",", "").split()
        grid[ps[1]] = ps[9:]
        flow = int(ps[4].split("=")[1][:-1])
        if flow > 0:
            flow_rate[ps[1]] = flow

    key_valves = ["AA"] + list(flow_rate.keys())
    reduced_grid = {}

    for v in key_valves:
        reduced_grid[v] = explore(v, key_valves, grid)

    to_visit = deque()
    to_visit.append(["AA"])
    pressure = set()

    while to_visit:
        current_path = to_visit.popleft()

        if get_time_elapsed(reduced_grid, current_path) > 30 or len(current_path) == len(key_valves):
            pressure.add(get_pressure(reduced_grid, flow_rate, current_path))
            continue

        for v in key_valves:
            if v not in current_path:
                n_path = [] + current_path + [v]

                to_visit.append(n_path)

    print(max(pressure))


@profiler
def part2():
    grid = {}
    flow_rate = {}

    for l in open("input.txt").read().splitlines():
        ps = l.replace(",", "").split()
        grid[ps[1]] = ps[9:]
        flow = int(ps[4].split("=")[1][:-1])
        if flow > 0:
            flow_rate[ps[1]] = flow

    key_valves = ["AA"] + list(flow_rate.keys())
    reduced_grid = {}

    for v in key_valves:
        reduced_grid[v] = explore(v, key_valves, grid)

    to_visit = deque()
    to_visit.append(["AA"])
    pressure = defaultdict(int)

    while to_visit:
        current_path = to_visit.popleft()

        if get_time_elapsed(reduced_grid, current_path) > 26 or len(current_path) >= len(key_valves) // 2:
            t = get_pressure(reduced_grid, flow_rate, current_path, 26)
            k = frozenset(set(current_path) - set(["AA"]))
            pressure[k] = max(t, pressure[k])
            continue

        for v in key_valves:
            if v not in current_path:
                n_path = [] + current_path + [v]

                to_visit.append(n_path)

    max_pressure = 0
    threshold = max(pressure.values()) * 0.75 

    for p1 in pressure:
        if pressure[p1] < threshold:
            continue
        for p2 in pressure:
            if pressure[p2] < threshold:
                continue
            if p1.isdisjoint(p2):
                max_pressure = max([max_pressure, pressure[p1] + pressure[p2]])
    print(max_pressure)


if __name__ == "__main__":

    part1()
    part2()
