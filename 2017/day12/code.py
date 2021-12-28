import time
from collections import Counter


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        method(*arg, **kw)
        print(
            "Method "
            + method.__name__
            + " took : "
            + "{:2.5f}".format(time.time() - t)
            + " sec"
        )

    return wrapper_method


@profiler
def part1():

    connections = {}

    for l in open("day12/input.txt").read().split("\n"):
        ps = l.split(" <-> ")
        connections[int(ps[0])] = list(map(int, ps[1].split(", ")))

    to_visit = [0]
    visited = set()

    while len(to_visit) > 0:
        c = to_visit.pop()

        visited.add(c)

        for n_c in connections[c]:
            if n_c not in visited:
                to_visit.append(n_c)

    print(len(visited))


def explore_node(graph, node):

    to_visit = [node]
    visited = set()

    while len(to_visit) > 0:
        c = to_visit.pop()

        visited.add(c)

        for n_c in graph[c]:
            if n_c not in visited:
                to_visit.append(n_c)

    return visited


@profiler
def part2():

    connections = {}

    for l in open("day12/input.txt").read().split("\n"):
        ps = l.split(" <-> ")
        connections[int(ps[0])] = list(map(int, ps[1].split(", ")))

    nodes = set(connections.keys())
    groups = []

    while len(nodes) > 0:
        c = nodes.pop()
        t = explore_node(connections, c)

        groups.append(c)

        nodes = nodes - t

    print(len(groups))


if __name__ == "__main__":

    part1()
    part2()
