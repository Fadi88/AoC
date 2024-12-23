# pylint: disable=C0114,C0116,C0301,C0209,W1514,C0414,E0001

from collections import deque
import networkx as nx
from typing import Any
import os
from time import perf_counter_ns
from collections import defaultdict
from itertools import combinations

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


@profiler
def part_1():
    data = defaultdict(set)
    with open(input_file) as f:
        for l in f.read().splitlines():
            ps = l.split("-")
            data[ps[0]].add(ps[1])
            data[ps[1]].add(ps[0])

    threes = set()
    for k in data:
        if k.startswith("t"):
            for c1, c2 in combinations(data[k], 2):
                if c1 in data[c2]:
                    threes.add(frozenset((k, c1, c2)))

    print(len(threes))
    print(len(data))


@profiler
def part_2():
    g = nx.Graph()

    with open(input_file) as f:
        for l in f.read().splitlines():
            ps = l.split("-")
            g.add_edge(ps[0], ps[1])

    clusters = list(nx.find_cliques_recursive(g))
    clusters.sort(key=len, reverse=True)
    clusters[0].sort()

    print(",".join(clusters[0]))


if __name__ == "__main__":
    part_1()
    part_2()
