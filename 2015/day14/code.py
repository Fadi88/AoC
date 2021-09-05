import time,re
from collections import defaultdict

def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print('Method '  + method.__name__ +' took : ' + "{:2.5f}".format(time.time()-t) + ' sec')
        return ret
    return wrapper_method

@profiler
def part1():

    deers = {}
    t = 2503
    with open('input.txt') as f:
        for l in f:
            p = l.strip().split()
            deers[p[0]] = (int(p[3]) , int(p[6]) , int(p[13]))

    race = {}
    for d in deers:
        p = deers[d]
        cycle = p[1] + p[2]
        dst = (t // cycle) * p[0] * p[1]
        if t%cycle > p[1]:
            dst += p[0] * p[1]
        else :
            dst += t%cycle * p[0]

        race[d] = dst

    print(max(race.values()))

@profiler
def part2():

    deers = {}
    t0 = 2503
    with open('input.txt') as f:
        for l in f:
            p = l.strip().split()
            deers[p[0]] = (int(p[3]) , int(p[6]) , int(p[13]))

    race_acc = defaultdict(int)
    
    for t in range(1,t0+1):

        race = {}

        for d in deers:
            p = deers[d]
            cycle = p[1] + p[2]
            dst = (t // cycle) * p[0] * p[1]
            if t%cycle > p[1]:
                dst += p[0] * p[1]
            else :
                dst += t%cycle * p[0]

            race[d] = dst

        m = max(race.values())

        for d in deers:
            if race[d] == m:
                race_acc[d] += 1
    
    print(max(race_acc.values()))

if __name__ == "__main__":

    part1()
    part2()
