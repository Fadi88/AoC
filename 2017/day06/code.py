import time
import math


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        method(*arg, **kw)
        print('Method ' + method.__name__ + ' took : ' +
              "{:2.5f}".format(time.time()-t) + ' sec')
    return wrapper_method


@profiler
def part1():

    inp = [* map(int, open('input.txt').read().strip().split())]

    seen = set()

    while str(inp) not in seen:
        seen.add(str(inp))

        val = max(inp)
        idx = inp.index(val)
        inp[idx] = 0

        for i in range(val):
            inp[(idx + i + 1) % len(inp)] += 1

    print(len(seen))


@profiler
def part2():

    inp = [* map(int, open('input.txt').read().strip().split())]

    seen = set()
    age = {}
    cnt = 0

    while str(inp) not in seen:
        seen.add(str(inp))

        age[str(inp)] = cnt
        cnt += 1

        val = max(inp)
        idx = inp.index(val)
        inp[idx] = 0

        for i in range(val):
            inp[(idx + i + 1) % len(inp)] += 1

    print(cnt-age[str(inp)])


if __name__ == "__main__":

    part1()
    part2()
