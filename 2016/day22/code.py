import time
import re
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

    grid = {}
    for l in open('input.txt').read().split('\n')[2:]:
        p = l.split()

        g = re.findall(r'-x(\d+)-y(\d+)',l)
        grid[(int(g[0][0]),int(g[0][1]))] = [int(p[1][:-1]) , int(p[2][:-1])]

    cnt = 0
    for i in grid:
        for o in grid:
            if o == i : continue
            a = grid[i]
            b = grid[o]

            if a[1] <= b[0] - b[1] and a[1] > 0:
                cnt += 1

    print(cnt)




@profiler
def part2():

    grid = {}
    for l in open('input.txt').read().split('\n')[2:]:
        p = l.split()

        g = re.findall(r'-x(\d+)-y(\d+)',l)
        grid[(int(g[0][0]),int(g[0][1]))] = [int(p[1][:-1]) , int(p[2][:-1])]


    for y in range(31):
        for x in range(33):
            if x == y == 0:
                c = '!'
            elif y == 0 and x == 32:
                c = 'G'
            else :
                a = grid[(x,y)]
                if a[1] == 0:
                    c = '_'
                elif a[1] > 100:
                    c = '#'
                else :
                    c = '.'

            print(c,end=' ')
        print()


if __name__ == "__main__":

    part1()
    part2()
