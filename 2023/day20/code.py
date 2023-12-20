# pylint: disable=C0114,C0116,C0301,C0209,W1514,C0206

from time import perf_counter
from collections import defaultdict
from math import prod


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print("Method " + method.__name__ + " took : " + "{:2.5f}".format(perf_counter() - t) + " sec")
        return ret

    return wrapper_method


class Module:
    def __init__(self, l) -> None:
        p = l.split(" -> ")
        self.name = p[0]
        if p[0][0] in "%&":
            self.type = p[0][0]
            self.name = "".join(p[0][1:])
        else:
            self.type = ""
            self.name = p[0]
        self.next = p[1].split(", ")
        self.state = False


@profiler
def part1():
    modules = {}
    for l in open("day20/input.txt").read().splitlines():
        m = Module(l)

        modules[m.name] = m

    for m in modules:
        if modules[m].type == "&":
            modules[m].input = {}
            for d in modules:
                if m in modules[d].next:
                    modules[m].input[d] = False

    high = 0
    lows = 0

    for _ in range(1000):
        to_send = [("broadcaster", False)]

        while to_send:
            src, sig = to_send.pop(0)

            dst = []
            output = sig

            if sig:
                high += 1
            else:
                lows += 1


            if src in modules and modules[src].type == "":
                dst = modules[src].next
            elif src in modules and modules[src].type == "%" and not sig:
                output = modules[src].state = not modules[src].state
                dst = modules[src].next
            elif src in modules and modules[src].type == "&":
                output = not all(modules[src].input.values())
                dst = modules[src].next

            for m in dst:
                to_send.append((m, output))
                if m in modules and modules[m].type == "&":
                    modules[m].input[src] = output

    print(high * lows)


@profiler
def part2():
    modules = {}
    for l in open("day20/input.txt").read().splitlines():
        m = Module(l)

        modules[m.name] = m
        if "rx" in m.next:
            main_module = m.name

    for m in modules:
        if modules[m].type == "&":
            modules[m].input = {}
            for d in modules:
                if m in modules[d].next:
                    modules[m].input[d] = False

    cycles = {m:0 for m in modules[main_module].input}

    cycle_cnt = 0
    while not all(cycles.values()):
        cycle_cnt += 1
        to_send = [("broadcaster", False)]

        while to_send:
            src, sig = to_send.pop(0)

            dst = []
            output = sig


            if src in modules and modules[src].type == "":
                dst = modules[src].next
            elif src in modules and modules[src].type == "%" and not sig:
                output = modules[src].state = not modules[src].state
                dst = modules[src].next
            elif src in modules and modules[src].type == "&":
                output = not all(modules[src].input.values())
                dst = modules[src].next

                if src == main_module and any(modules[src].input.values()):
                    for m in modules[src].input:
                        if modules[src].input[m]:
                            cycles[m] = cycle_cnt

            for m in dst:
                to_send.append((m, output))
                if m in modules and modules[m].type == "&":
                    modules[m].input[src] = output

    print(prod(cycles.values()))

if __name__ == "__main__":
    part1()
    part2()
