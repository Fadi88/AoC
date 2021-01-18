import time
from itertools import combinations, permutations


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print('Method ' + method.__name__ + ' took : ' +
              "{:2.5f}".format(time.time()-t) + ' sec')
        return ret
    return wrapper_method


def find_shortest_path(p1, p2, grid):
    to_visit = [[p1]]
    seen = set()
    seen.add(p1)

    while to_visit:
        path = to_visit.pop(0)

        for d in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            n_p = (path[-1][0] + d[0], path[-1][1] + d[1])
            if n_p == p2:
                return len(path)
            elif n_p in grid and n_p not in seen:
                new_path = path.copy()
                new_path.append(n_p)
                to_visit.append(new_path)
                seen.add(n_p)

    return -1


@profiler
def part1():

    free_space = set()
    goals = set()

    y = 0
    for l in open('input.txt').read().split('\n'):
        x = 0
        for c in l:
            if c == '.':
                free_space.add((x, y))
            elif c != '#':
                goals.add((x, y))
                free_space.add((x, y))
                if c == '0':
                    p0 = (x, y)
            x += 1
        y += 1

    dsts = {}
    for p in goals:
        dsts[p] = {}

    for p1, p2 in permutations(goals, 2):
        dsts[p1][p2] = find_shortest_path(p1, p2, free_space)

    paths = []
    goals.remove(p0)
    for p in permutations(goals):
        dst = 0
        p = (p0, *p)
        for i in range(len(p) - 1):
            dst += dsts[p[i]][p[i+1]]

        paths.append(dst)

    print(min(paths))


@profiler
def part2():

    free_space = set()
    goals = set()

    y = 0
    for l in open('input.txt').read().split('\n'):
        x = 0
        for c in l:
            if c == '.':
                free_space.add((x, y))
            elif c != '#':
                goals.add((x, y))
                free_space.add((x, y))
                if c == '0':
                    p0 = (x, y)
            x += 1
        y += 1

    dsts = {}
    for p in goals:
        dsts[p] = {}

    for p1, p2 in permutations(goals, 2):
        dsts[p1][p2] = find_shortest_path(p1, p2, free_space)

    paths = []
    goals.remove(p0)
    for p in permutations(goals):
        dst = 0
        p = (p0, *p)
        for i in range(len(p) - 1):
            dst += dsts[p[i]][p[i+1]]

        paths.append(dst + dsts[p[-1]][p0]) # adding distance to retrun to 0 for every path

    print(min(paths))


if __name__ == "__main__":

    part1()
    part2()
