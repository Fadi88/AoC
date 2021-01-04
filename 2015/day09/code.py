import time,os,re
from collections import defaultdict
from itertools import permutations  

def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print('Method '  + method.__name__ +' took : ' + "{:2.5f}".format(time.time()-t) + ' sec')
        return ret
    return wrapper_method

@profiler
def part1():
    with open('input.txt', 'r') as f:
        dsts = {}
        places = set()
        for l in f:
            l = l.strip()
            p = l.split(' = ')
            t = p[0].split(' to ')
            t.sort()
            places.update(t)
            dsts[tuple(t)] = int(p[1])

        min_dist = 1000000

        for rt in permutations(places):
            dst = 0
            for i in range(len(rt) - 1):
                t = [rt[i] , rt[i+1] ]
                t.sort()
                dst += dsts[tuple(t)]

            if dst < min_dist : min_dist = dst

        print(min_dist)

@profiler
def part2():
    with open('input.txt', 'r') as f:
        dsts = {}
        places = set()
        for l in f:
            l = l.strip()
            p = l.split(' = ')
            t = p[0].split(' to ')
            t.sort()
            places.update(t)
            dsts[tuple(t)] = int(p[1])

        max_dist = 0

        for rt in permutations(places):
            dst = 0
            for i in range(len(rt) - 1):
                t = [rt[i] , rt[i+1] ]
                t.sort()
                dst += dsts[tuple(t)]

            if dst > max_dist : max_dist = dst

        print(max_dist)

if __name__ == "__main__":

    part1()
    part2()
