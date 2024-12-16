# pylint: disable=C0114,C0116,C0301,C0209,W1514,C0414,E0001

import heapq
from typing import Any
import os
from time import perf_counter_ns

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
    deltas = {
        ">": (1, 0),
        "v": (0, 1),
        "<": (-1, 0),
        "^": (0, -1),
    }
    rot = ">v<^"

    to_visit = []
    visited = {
        (start, ">"): 0,

    }

    heapq.heappush(to_visit, (0, ">", start))

    while to_visit:
        score, cd, (cx, cy) = heapq.heappop(to_visit)

        if ((cx, cy), cd) in visited and visited[((cx, cy), cd)] < score:
            continue

        dx, dy = deltas[cd]
        # try forward
        if (cx+dx, cy+dy) in free_spaces:
            np = (cx+dx, cy+dy)
            if (np, cd) not in visited or visited[(np, cd)] > score + 1:
                visited[(np, cd)] = score + 1
                heapq.heappush(to_visit, (score+1, cd, np))

        # try turn
        for dr in [-1, 1]:
            nd = rot[(rot.index(cd) + dr) % 4]
            if ((cx, cy), nd) not in visited or visited[((cx, cy), nd)] > score + 1000:
                visited[((cx, cy), nd)] = score + 1000
                heapq.heappush(to_visit, (score+1000, nd, (cx, cy)))

    return visited


@profiler
def part_1():

    start = (-1, -1)
    free_spaces = set()

    with open(input_file) as f:
        for y, l in enumerate(f):
            for x, c in enumerate(l.strip()):
                if c == "E":
                    end = (x, y)
                    free_spaces.add((x, y))
                elif c == "S":
                    start = (x, y)
                elif c == ".":
                    free_spaces.add((x, y))

    visited = dijkstra(start, free_spaces)
    print(min(v for k, v in visited.items() if k[0] == end))


def back_track(visited, target_state):
    deltas = {
        ">": (1, 0),
        "v": (0, 1),
        "<": (-1, 0),
        "^": (0, -1),
    }
    rot = ">v<^"
    to_visit = [(target_state)]

    seen = set()
    while to_visit:
        cp, cd = to_visit.pop(0)

        seen.add(cp)
        # try back forward
        dx, dy = deltas[cd]
        np = (cp[0]-dx, cp[1]-dy)
        if (np, cd) in visited and visited[(np, cd)] + 1 == visited[(cp, cd)]:
            to_visit.append((np, cd))
        # try rotate
        nd1 = rot[(rot.index(cd) + 1) % 4]
        nd2 = rot[(rot.index(cd) - 1) % 4]

        if (cp, nd1) in visited and visited[(cp, nd1)] + 1000 == visited[(cp, cd)]:
            to_visit.append((cp, nd1))
        if (cp, nd2) in visited and visited[(cp, nd2)] + 1000 == visited[(cp, cd)]:
            to_visit.append((cp, nd2))

    return seen


@profiler
def part_2():

    start = (-1, -1)
    free_spaces = set()

    with open(input_file) as f:
        for y, l in enumerate(f):
            for x, c in enumerate(l.strip()):
                if c == "E":
                    end = (x, y)
                    free_spaces.add((x, y))
                elif c == "S":
                    start = (x, y)
                elif c == ".":
                    free_spaces.add((x, y))

    visited = dijkstra(start, free_spaces)

    # back track from end with lowest cost
    target_score = min(v for k, v in visited.items() if k[0] == end)
    target_state = [k for k, v in visited.items() if v ==
                    target_score and k[0] == end][0]

    print(len(back_track(visited, target_state)))


if __name__ == "__main__":
    part_1()
    part_2()
