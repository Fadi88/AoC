import time
from collections import Counter


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print(
            "Method "
            + method.__name__
            + " took : "
            + "{:2.5f}".format(time.time() - t)
            + " sec"
        )
        return ret
    return wrapper_method


@profiler
def part1():

    firewall = {}

    for l in open("day13/input.txt").read().split("\n"):
        ps = l.split(": ")
        firewall[int(ps[0])] = int(ps[1])

    print(sum([s * firewall[s] for s in firewall if s%(2*firewall[s] - 2) == 0]))
        



@profiler
def part2():

    firewall = {}

    for l in open("day13/input.txt").read().split("\n"):
        ps = l.split(": ")
        firewall[int(ps[0])] = int(ps[1])

if __name__ == "__main__":

    part1()
    part2()

from itertools import count as c
@profiler
def solve(input):
    S = [(d, r, 2*r-2) for d, r in eval(input.strip().replace(*'\n,').join('{}')).items()]
    part1 = sum(d*r for d, r, R in S if not d%R)
    part2 = next(i for i in c() if all((i+d)%R for d, _, R in S))
    return part1, part2

print(solve(open("day13/input.txt").read()))
