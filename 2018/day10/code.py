import time
import re
import math


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


def sim(p, t):
    return (p[0] + p[2] * t, p[1] + p[3] * t)


@profiler
def part_1_2():
    particles = []
    for l in open("day10/input.txt"):
        particles.append(tuple(map(int, re.findall(r"(-?\d+)", l.strip()))))

    t = 0

    d = set(map(lambda p: sim(p, 0), particles))
    entropy = (max([p[0] for p in d]) - min([p[0] for p in d])) * (
        max([p[1] for p in d]) - min([p[1] for p in d])
    )
    while True:
        t += 1
        n_d = set(map(lambda p: sim(p, t), particles))
        n_entropy = (max([p[0] for p in n_d]) - min([p[0] for p in n_d])) * (
            max([p[1] for p in n_d]) - min([p[1] for p in n_d])
        )

        if n_entropy > entropy:
            break
        d = n_d
        entropy = n_entropy

    print(max([p[0] for p in d]), min([p[0] for p in d]))
    for y in range(min([p[1] for p in d]), max([p[1] for p in d]) + 1):
        for x in range(min([p[0] for p in d]), max([p[0] for p in d]) + 1):
            if (x, y) in d:
                print("#", end="")
            else:
                print(" ", end="")
        print()
    print(t - 1)


if __name__ == "__main__":

    part_1_2()
