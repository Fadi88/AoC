import time
from collections import defaultdict
from math import sqrt
from itertools import combinations, permutations


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


def distance(p1, p2):
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    dz = p1[2] - p2[2]

    return int(sqrt(dx * dx + dy * dy + dz * dz))


def distance_taxi(p1, p2):
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    dz = p1[2] - p2[2]

    return abs(dx) + abs(dy) + abs(dz)


def get_common_pt_num(config, s0, s1):
    return max(
        [
            len(config[s0][p0].intersection(config[s1][p1]))
            for p0 in config[s0]
            for p1 in config[s1]
        ]
    )


def allign(config1, config2):
    mapping = {}
    for p1 in config1:
        for p2 in config2:
            if len(config1[p1].intersection(config2[p2])) > 10:
                mapping[p1] = p2

    cog_1_x = sum([k[0] for k in mapping.keys()]) / len(mapping.keys())
    cog_1_y = sum([k[1] for k in mapping.keys()]) / len(mapping.keys())
    cog_1_z = sum([k[2] for k in mapping.keys()]) / len(mapping.keys())

    cog_2_x = sum([k[0] for k in mapping.values()]) / len(mapping.values())
    cog_2_y = sum([k[1] for k in mapping.values()]) / len(mapping.values())
    cog_2_z = sum([k[2] for k in mapping.values()]) / len(mapping.values())

    p1 = list(mapping.keys())[0]
    p2 = mapping[p1]

    p1_mod = (round(p1[0] - cog_1_x), round(p1[1] - cog_1_y), round(p1[2] - cog_1_z))
    p2_mod = (round(p2[0] - cog_2_x), round(p2[1] - cog_2_y), round(p2[2] - cog_2_z))

    rot = {}
    for i in range(3):
        idx = list(map(abs, p2_mod)).index(abs(p1_mod[i]))
        rot[i] = (idx, p1_mod[i] // p2_mod[idx])

    p2_rot = [0] * 3
    for i in range(3):
        p2_rot[i] = p2[rot[i][0]] * rot[i][1]

    translation = []
    for i in range(3):
        translation.append(p2_rot[i] -  p1[i])

    return rot,translation


@profiler
def part1():
    input = open("day19/input.txt").read().split("\n\n")
    scanners = [
        list(map(lambda x: tuple(map(int, x.split(","))), s.split("\n")[1:]))
        for s in input
    ]

    config = []

    for s in range(len(scanners)):
        dist = defaultdict(set)
        for p1 in scanners[s]:
            for p2 in scanners[s]:
                dist[p1].add(distance(p1, p2))
            dist[p1].remove(0)
        config.append(dist)

    common = []
    for s0 in range(len(scanners)):
        tmp = []
        for s1 in range(len(scanners)):
            if s0 == s1:
                tmp.append(-1)
            else:
                tmp.append(get_common_pt_num(config, s0, s1))
        common.append(tmp)

    allign(config[0], config[7])


@profiler
def part2():
    pass


if __name__ == "__main__":

    part1()
    part2()
