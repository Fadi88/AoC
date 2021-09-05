import time
import re
from collections import defaultdict,deque


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print('Method ' + method.__name__ + ' took : ' +
              "{:2.5f}".format(time.time()-t) + ' sec')
        return ret
    return wrapper_method


def replacenth(string, sub, wanted, n):
    where = [m.start() for m in re.finditer(sub, string)][n-1]
    before = string[:where]
    after = string[where:]
    after = after.replace(sub, wanted, 1)
    newString = before + after
    return newString


@profiler
def part1():

    with open('input.txt') as f:
        ls, m = f.read().split('\n\n')

    m = m.strip()
    tra = defaultdict(list)
    for l in ls.split('\n'):
        p = l.strip().split(' => ')
        tra[p[0]].append(p[1])

    comb = set()

    for d in tra:
        for n in tra[d]:
            for i in range(m.count(d)):
                comb.add(replacenth(m, d, n, i+1))

    print(len(comb))


@profiler
def part2():

    with open('input.txt') as f:
        ls, m = f.read().split('\n\n')

    m = m.strip()
    tra = {}
    for l in ls.split('\n'):
        p = l.strip().split(' => ')
        tra[p[1]] = p[0]

    cnt = 0

    while m != 'e':
        for e in tra:
            cnt += m.count(e)
            m = m.replace(e,tra[e])

    print(cnt)

if __name__ == "__main__":

    part1()
    part2()

