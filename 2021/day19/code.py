import time
from collections import defaultdict
from math import sqrt
from itertools import combinations


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


def get_common_pt_num(config_1, config_2):
    return max(
        [
            len(config_1[p0].intersection(config_2[p1]))
            for p0 in config_1
            for p1 in config_2
        ]
    )


def get_config(sensor_data):
    config = defaultdict(set)
    for p1 in sensor_data:
        for p2 in sensor_data:
            config[p1].add(distance(p1, p2))
        config[p1].remove(0)

    return config


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
        translation.append(p2_rot[i] - p1[i])

    return rot, translation


def transform_points(rot, trans, points):
    new_points = set()

    for p in points:
        new_points.add(tuple(p[rot[i][0]] * rot[i][1] - trans[i] for i in range(3)))

    return new_points


@profiler
def part1():
    input = open("day19/input.txt").read().split("\n\n")
    scanners = [
        list(map(lambda x: tuple(map(int, x.split(","))), s.split("\n")[1:]))
        for s in input
    ]

    grid = set(scanners.pop(0))

    scanner_pos = []
    while len(scanners) > 0:
        grid_config = get_config(grid)
        scaners_common = [
            get_common_pt_num(grid_config, get_config(s)) for s in scanners
        ]

        s = scaners_common.index(max(scaners_common))

        rot, trams = allign(grid_config, get_config(scanners[s]))
        grid.update(transform_points(rot, trams, scanners[s]))

        del scanners[s]
        scanner_pos.append(trams)

    print(len(grid))
    return scanner_pos


@profiler
def part2(scanner_pos):
    print(max([distance_taxi(c[0],c[1]) for c in combinations(scanner_pos,2)]))


if __name__ == "__main__":

    scanner_pos = part1()
    part2(scanner_pos)
