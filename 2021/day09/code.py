import time
from collections import deque


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print('Method ' + method.__name__ + ' took : ' +
              "{:2.5f}".format(time.time()-t) + ' sec')
        return ret
    return wrapper_method


@profiler
def part1():
    deltas = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    heightmap = [list(map(int, list(l.strip())))
                 for l in open("day09/input.txt")]

    total = 0
    for x in range(len(heightmap)):
        for y in range(len(heightmap[x])):
            if all([heightmap[x][y] < heightmap[x+dx][y+dy] for dx, dy in deltas if 0 <= x+dx < len(heightmap) and 0 <= y+dy < len(heightmap[x])]):
                total += 1 + heightmap[x][y]

    print("part 1 : ", total)


def discover_point(x, y, heightmap, visited):
    deltas = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    to_visit = deque(((x, y),))
    ret = set()
    while to_visit:
        cx, cy = to_visit.popleft()
        visited.add((cx, cy))
        if heightmap[cx][cy] < 9:
            ret.add((cx, cy))
            for dx, dy in deltas:
                if 0 <= cx+dx < len(heightmap) and 0 <= cy+dy < len(heightmap[cx]) and (cx+dx, cy+dy) not in visited:
                    to_visit.append((cx+dx, cy+dy))

    return len(ret)


@profiler
def part2():
    heightmap = []
    deltas = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    heightmap = [list(map(int, list(l.strip())))
                 for l in open("day09/input.txt")]

    sinks_size = []
    visited = set()

    for x in range(len(heightmap)):
        for y in range(len(heightmap[x])):
            if (x, y) not in visited:
                sinks_size.append(discover_point(x, y, heightmap, visited))
                visited.add((x, y))

    total = sorted(sinks_size)[-3:]

    print("part 2 : ", total[0] * total[1] * total[2])


if __name__ == "__main__":

    part1()
    part2()
