import time
import re
from collections import defaultdict


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print('Method ' + method.__name__ + ' took : ' +
              "{:2.5f}".format(time.time()-t) + ' sec')
        return ret
    return wrapper_method


def is_open(x, y):
    inp = 1350
    b_rep = bin(x*x + 3*x + 2*x*y + y + y*y + inp)
    return b_rep.count('1') % 2 == 0


@profiler
def part1():

    trg = (31, 39)

    deltas = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    to_visit = [[(1, 1)]]
    visited = set()
    visited.add((1, 1))

    while to_visit:
        path = to_visit.pop(0)
        last_pt = path[-1]

        for d in deltas:
            nx = last_pt[0] + d[0]
            ny = last_pt[1] + d[1]

            if (nx, ny) == trg:
                print(len(path))
                break
            new_path = path.copy()
            if nx >= 0 and ny >= 0 and is_open(nx, ny) and (nx, ny) not in visited:
                new_path.append((nx, ny))
                to_visit.append(new_path)
                visited.add((nx, ny))


@profiler
def part2():

    deltas = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    to_visit = [[(1, 1)]]
    visited = set()
    visited.add((1, 1))

    cnt = 1  # visitor area
    while to_visit:
        path = to_visit.pop(0)
        last_pt = path[-1]

        if len(path) < 51:
            cnt += 1
        else:
            break

        for d in deltas:
            nx = last_pt[0] + d[0]
            ny = last_pt[1] + d[1]

            new_path = path.copy()
            if nx >= 0 and ny >= 0 and is_open(nx, ny) and (nx, ny) not in visited:
                new_path.append((nx, ny))
                to_visit.append(new_path)
                visited.add((nx, ny))

    print(cnt)


if __name__ == "__main__":

    part1()
    part2()
