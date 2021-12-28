import time
import re
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


@profiler
def part1():

    inst = open("day16/input.txt").read().split(",")

    prg = deque([chr(ord("a") + i) for i in range(16)])

    for i in inst:
        if i[0] == "p":
            i1 = prg.index(i[1])
            i2 = prg.index(i[-1])

            prg[i1] = i[-1]
            prg[i2] = i[1]
        elif i[0] == "s":
            prg.rotate(int(i[1:]))
        elif i[0] == "x":
            idx = re.findall(r"(\d+)", i)
            tmp = prg[int(idx[0])]
            prg[int(idx[0])] = prg[int(idx[1])]
            prg[int(idx[1])] = tmp

    print("".join(prg))


@profiler
def part2():

    inst = open("day16/input.txt").read().split(",")

    seen = {}
    cnt = 0

    prg = deque([chr(ord("a") + i) for i in range(16)])

    while True:
        for i in inst:
            if i[0] == "p":
                i1 = prg.index(i[1])
                i2 = prg.index(i[-1])

                prg[i1] = i[-1]
                prg[i2] = i[1]
            elif i[0] == "s":
                prg.rotate(int(i[1:]))
            elif i[0] == "x":
                idx = re.findall(r"(\d+)", i)
                tmp = prg[int(idx[0])]
                prg[int(idx[0])] = prg[int(idx[1])]
                prg[int(idx[1])] = tmp

        t = "".join(prg)

        if t in seen.values():
            break
        seen[cnt] = t
        cnt += 1

    print(seen[1000000000 % len(seen) - 1])


if __name__ == "__main__":

    part1()
    part2()
