import time
import re
import hashlib


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
    inp = 'dmypynyp'

    to_visit = [[inp, 0, 0]]

    doors = {0: 'U', 1: 'D', 2: 'L', 3: 'R'}
    deltas = {'U': (0, -1), 'D': (0, 1), 'L': (-1, 0), 'R': (1, 0)}

    
    while to_visit:
        st, x, y = to_visit.pop(0)
        h = hashlib.md5(bytes(st, 'utf-8')).hexdigest()

        for i in range(4):
            if h[i] in ['b', 'c', 'd', 'e', 'f']:
                door = doors[i]
                delta = deltas[door]
                nx, ny = x + delta[0], y + delta[1]
                if nx in [0, 1, 2, 3] and ny in [0, 1, 2, 3] and (nx, ny) :
                    n_st = st + door
                    to_visit.append([n_st, nx, ny])

                if nx == 3 and ny == 3:
                    print(n_st[len(inp):])
                    return



@profiler
def part2():
    inp = 'dmypynyp'

    to_visit = [[inp, 0, 0]]

    doors = {0: 'U', 1: 'D', 2: 'L', 3: 'R'}
    deltas = {'U': (0, -1), 'D': (0, 1), 'L': (-1, 0), 'R': (1, 0)}

    sol = []
    while to_visit:
        st, x, y = to_visit.pop(0)
        h = hashlib.md5(bytes(st, 'utf-8')).hexdigest()

        for i in range(4):
            if h[i] in ['b', 'c', 'd', 'e', 'f']:
                door = doors[i]
                delta = deltas[door]
                nx, ny = x + delta[0], y + delta[1]
                if nx in [0, 1, 2, 3] and ny in [0, 1, 2, 3] and (nx, ny):
                    n_st = st + door
                    if nx == 3 and ny == 3:
                        sol.append(len(n_st) - len(inp))
                    else :
                        to_visit.append([n_st, nx, ny])

    print(max(sol))


if __name__ == "__main__":

    part1()
    part2()
