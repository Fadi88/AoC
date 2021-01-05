import time,re
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

    heat = defaultdict(dict)
    ppl = set()
    with open('input.txt') as f:
        for l in f:
            s = 1
            p = l.strip().split()
            ppl.add(p[0])
            if 'lose' in l : s = -1
            heat[p[0]][p[-1][:-1]] = s * int(p[3])

    happ = 0
    for s in permutations(ppl):
        tmp = sum([ heat[s[i]][s[i-1]] +  heat[s[i]][s[i+1]] for i in range(1,len(s)-1)])
        tmp += heat[s[0]][s[1]] + heat[s[0]][s[-1]]
        tmp += heat[s[-1]][s[0]] + heat[s[-1]][s[-2]]

        if tmp > happ : happ = tmp
    print(happ)


@profiler
def part2():

    heat = defaultdict(dict)
    ppl = set()
    with open('input.txt') as f:
        for l in f:
            s = 1
            p = l.strip().split()
            ppl.add(p[0])
            if 'lose' in l : s = -1
            heat[p[0]][p[-1][:-1]] = s * int(p[3])

    for d in ppl:
        heat[d]['me'] = 0

    ppl.add('me')
    heat['me'] = defaultdict(int)

    happ = 0
    for s in permutations(ppl):
        tmp = sum([ heat[s[i]][s[i-1]] +  heat[s[i]][s[i+1]] for i in range(1,len(s)-1)])
        tmp += heat[s[0]][s[1]] + heat[s[0]][s[-1]]
        tmp += heat[s[-1]][s[0]] + heat[s[-1]][s[-2]]

        if tmp > happ : happ = tmp

    print(happ)

if __name__ == "__main__":

    part1()
    part2()
