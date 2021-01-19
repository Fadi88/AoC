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

    reg = defaultdict(int)

    for l in open('input.txt'):
        p = l.strip().split()
        val = int(p[2]) if 'inc' in l else -int(p[2])
        
        if eval('reg[\''+str(p[-3]) +'\'] ' + ' '.join(p[-2:])):
            reg[p[0]] += val

    print(max(reg.values()))
        

@profiler
def part2():

    reg = defaultdict(int)
    highest = 0

    for l in open('input.txt'):
        p = l.strip().split()
        val = int(p[2]) if 'inc' in l else -int(p[2])
        
        if eval('reg[\''+str(p[-3]) +'\'] ' + ' '.join(p[-2:])):
            reg[p[0]] += val
            if reg[p[0]] > highest:
                highest = reg[p[0]]

    print(highest)


if __name__ == "__main__":

    part1()
    part2()
