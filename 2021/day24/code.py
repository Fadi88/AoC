import time


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
    fs = open("day24/input.txt").read().split("inp w")
    fs = list(map(lambda x: x.split("\n")[1:], fs))[1:]

    mapping = {}

    z = []
    for idx in range(len(fs)):
        p1, p2, p3 = (
            int(fs[idx][3].split(" ")[2]),
            int(fs[idx][4].split(" ")[2]),
            int(fs[idx][14].split(" ")[2]),
        )
        if p1 == 1:
            z.append((idx, p3))
        elif p1 == 26:
            mapping[(idx, p2)] = z.pop()
        else:
            assert False

    z = [9] * len(fs)

    for p in mapping:
        delta = mapping[p][1] + p[1]
        # target
        # z[mapping[p][0]]  + mapping[p][1] + p[1] == z[p[0]]
        if delta < 0:
            z[p[0]] = 9 + delta
        else:
            z[mapping[p][0]] = 9 - delta

    print("".join(map(str, z)))


@profiler
def part2():
    fs = open("day24/input.txt").read().split("inp w")
    fs = list(map(lambda x: x.split("\n")[1:], fs))[1:]

    mapping = {}

    z = []
    for idx in range(len(fs)):
        p1, p2, p3 = (
            int(fs[idx][3].split(" ")[2]),
            int(fs[idx][4].split(" ")[2]),
            int(fs[idx][14].split(" ")[2]),
        )
        if p1 == 1:
            z.append((idx, p3))
        elif p1 == 26:
            mapping[(idx, p2)] = z.pop()
        else:
            assert False

    z = [1] * len(fs)

    for p in mapping:
        delta = mapping[p][1] + p[1]
        # target
        # z[mapping[p][0]]  + mapping[p][1] + p[1] == z[p[0]]
        if delta < 0:
            z[mapping[p][0]] = 1 - delta
        else:
            z[p[0]] = 1 + delta

    print("".join(map(str, z)))


if __name__ == "__main__":

    part1()
    part2()
