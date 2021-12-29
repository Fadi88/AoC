import time
from collections import deque


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


input = 314


@profiler
def part1():

    buff = deque([0])

    pos = 0
    for i in range(1, 2017 + 1):
        pos = (pos + input) % i
        buff.insert(pos + 1, i)

        pos += 1

    print(buff[buff.index(2017) + 1])


@profiler
def part2():

    pos = 0
    for i in range(1, 50000000 + 1):
        pos = (pos + input) % i
        if pos == 0:
            t = i

        pos += 1

    print(t)


if __name__ == "__main__":

    part1()
    part2()
