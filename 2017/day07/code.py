import time
from collections import defaultdict


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        method(*arg, **kw)
        print('Method ' + method.__name__ + ' took : ' +
              "{:2.5f}".format(time.time()-t) + ' sec')
    return wrapper_method


@profiler
def part1():

    towers = defaultdict(list)

    for l in open('input.txt'):
        l = l.strip()
        p = l.split()
        if '->' in l:
            towers[p[0]] = l[l.find('->') + 3:].split(', ')
        else:
            towers[p[0]] = []

    leaves = []
    for ele in towers:
        leaves += towers[ele]

    for ele in towers:
        if ele not in leaves:
            print(ele)
            break


def get_weight(towers,weights,prog):
    if len(towers[prog]) == 0:
        return weights[prog]
    else :
        w = weights[prog]
        for sub in towers[prog]:
            w += get_weight(towers,weights,sub)
        return w

@profiler
def part2():

    towers = defaultdict(list)
    weights = {}

    for l in open('input.txt'):
        l = l.strip()
        p = l.split()
        weights[p[0]] = int(p[1][1:-1])
        if '->' in l:
            towers[p[0]] = l[l.find('->') + 3:].split(', ')
        else:
            towers[p[0]] = []

    leaves = []
    for ele in towers:
        leaves += towers[ele]

    for ele in towers:
        if ele not in leaves:
            root = ele
            break

    diff = 0
    while True:
        tmp = [get_weight(towers,weights,p) for p in towers[root]]
        same = [tmp.count(tmp[i]) > 1 for i in range(len(tmp))]
        if not all(same):
            root = towers[root][same.index(False)]
            diff = tmp[same.index(False)] - tmp[(same.index(False) + 1)% len(tmp)] 
        else:
            print(weights[root] - diff)
            break

if __name__ == "__main__":

    part1()
    part2()
