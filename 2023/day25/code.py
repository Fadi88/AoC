from time import perf_counter
import networkx


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print("Method " + method.__name__ + " took : " + "{:2.5f}".format(perf_counter() - t) + " sec")
        return ret

    return wrapper_method


@profiler
def part1():
    graph = networkx.Graph()

    for l in open("day25/input.txt"):
        src, dst = l.strip().split(": ")

        for n in dst.split():
            graph.add_edge(src, n)

    _, partitions = networkx.stoer_wagner(graph)

    print(len(partitions[0]) * len(partitions[1]))


if __name__ == "__main__":
    part1()
