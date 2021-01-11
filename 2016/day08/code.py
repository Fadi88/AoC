import time
import os
import re


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        method(*arg, **kw)
        print('Method ' + method.__name__ + ' took : ' +
              "{:2.5f}".format(time.time()-t) + ' sec')
    return wrapper_method


def print_grid(grid):
    for y in range(6):
        for x in range(50):
            ch = '#' if (x, y) in grid else ' '
            print(ch, end='')
        print()


@profiler
def part1():
    cnt = 0
    for l in open('input.txt').read().split('\n'):
        if 'rect' in l:
            cnt += eval(l.split()[1].replace('x', '*'))

    print(cnt)


@profiler
def part2():

    grid = set()

    for l in open('input.txt').read().split('\n'):
        if 'rect' in l:
            dim = list(map(int, l.split()[1].split('x')))
            for x in range(dim[0]):
                for y in range(dim[1]):
                    grid.add((x, y))

        elif 'row' in l:
            rot = list(map(int, re.findall(r'\d+', l)))
            tmp = set()
            for p in grid:
                if p[1] != rot[0]:
                    tmp.add(p)
                else:
                    tmp.add(((p[0] + rot[1]) % 50, rot[0]))
            grid = tmp

        elif 'column' in l:
            rot = list(map(int, re.findall(r'\d+', l)))
            tmp = set()
            for p in grid:
                if p[0] != rot[0]:
                    tmp.add(p)
                else:
                    tmp.add((p[0], (p[1]+rot[1]) % 6))
            grid = tmp

    print_grid(grid)


if __name__ == "__main__":

    # part1()
    part2()
