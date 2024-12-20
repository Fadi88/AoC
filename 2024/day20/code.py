# pylint: disable=C0114,C0116,C0301,C0209,W1514,C0414,E0001


from itertools import product
from typing import Any
import os
from time import perf_counter_ns
import heapq

input_file = os.path.join(os.path.dirname(__file__), "input.txt")
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


def dijkstra(start, free_spaces):
    to_visit = []
    visited = {
        (start): 0,
    }

    heapq.heappush(to_visit, (0, start))

    while to_visit:
        score, (cx, cy) = heapq.heappop(to_visit)

        if (cx, cy) in visited and visited[(cx, cy)] < score:
            continue

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            if (cx+dx, cy+dy) in free_spaces:
                np = (cx+dx, cy+dy)
                if np not in visited or visited[np] > score + 1:
                    visited[np] = score + 1
                    heapq.heappush(to_visit, (score+1, np))

    return visited


def get_savings(distances, jump_size, free_space):
    ret = 0
    for p in free_space:
        for dx, dy in product(range(-jump_size, jump_size+1), repeat=2):
            if dx == dy == 0 or abs(dx) + abs(dy) > jump_size:
                continue
            np = (p[0]+dx, p[1]+dy)
            if np in free_space:
                no_walls_cost = abs(p[0]-np[0]) + abs(p[1]-np[1])
                all_walls_cost = distances[np] - distances[p]

                if (all_walls_cost - no_walls_cost) >= 100:
                    ret += 1
    return ret


@profiler
def part_1():
    free_space = set()
    end = None
    with open(input_file) as f:
        for y, line in enumerate(f):
            for x, c in enumerate(line):
                if c in ".SE":
                    free_space.add((x, y))
                if c == "E":
                    end = (x, y)

    from_end = dijkstra(end, free_space)

    print(get_savings(from_end, 2, free_space))


@profiler
def part_2():
    free_space = set()
    end = None
    with open(input_file) as f:
        for y, line in enumerate(f):
            for x, c in enumerate(line):
                if c in ".SE":
                    free_space.add((x, y))
                if c == "E":
                    end = (x, y)

    from_end = dijkstra(end, free_space)

    print(get_savings(from_end, 20, free_space))


if __name__ == "__main__":
    part_1()
    part_2()
