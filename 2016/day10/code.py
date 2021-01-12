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


@profiler
def part1():

    plan = {}
    bots = defaultdict(list)
    outputs = defaultdict(list)

    for l in open('input.txt').read().split('\n'):
        if 'value' in l:
            p = re.findall(r'\d+', l)
            bots[int(p[1])].append(int(p[0]))
            bots[int(p[1])].sort()

        else:
            p = l.split()
            plan[int(p[1])] = [p[5]+' '+p[6], p[10]+' '+p[11]]

    while True:
        k = bots.keys()
        for ele in list(k):
            if len(bots[ele]) == 2:

                h_val = bots[ele].pop()
                l_val = bots[ele].pop()

                if l_val in [17, 61] and h_val in [17, 61]:
                    print(ele)
                    return
                l_trg = plan[ele][0]
                h_trg = plan[ele][1]

                if 'output' in h_trg:
                    outputs[int(h_trg.split()[1])].append(h_val)
                else:
                    bots[int(h_trg.split()[1])].append(h_val)
                    bots[int(h_trg.split()[1])].sort()

                if 'output' in l_trg:
                    outputs[int(l_trg.split()[1])].append(l_val)
                else:
                    bots[int(l_trg.split()[1])].append(l_val)
                    bots[int(l_trg.split()[1])].sort()


@profiler
def part2():

    plan = {}
    bots = defaultdict(list)
    outputs = defaultdict(list)

    for l in open('input.txt').read().split('\n'):

        if 'value' in l:
            p = re.findall(r'\d+', l)
            bots[int(p[1])].append(int(p[0]))
            bots[int(p[1])].sort()
        else:
            p = l.split()
            plan[int(p[1])] = [p[5]+' '+p[6], p[10]+' '+p[11]]

    while True:
        k = bots.keys()
        for ele in list(k):
            if len(bots[ele]) == 2:
                h_val = bots[ele].pop()
                l_val = bots[ele].pop()
                l_trg = plan[ele][0]
                h_trg = plan[ele][1]

                if 'output' in h_trg:
                    outputs[int(h_trg.split()[1])].append(h_val)
                else:
                    bots[int(h_trg.split()[1])].append(h_val)
                    bots[int(h_trg.split()[1])].sort()

                if 'output' in l_trg:
                    outputs[int(l_trg.split()[1])].append(l_val)
                else:
                    bots[int(l_trg.split()[1])].append(l_val)
                    bots[int(l_trg.split()[1])].sort()

                if 0 in outputs and 1 in outputs and 2 in outputs:
                    print(outputs[0][0]*outputs[1][0]*outputs[2][0])
                    return


if __name__ == "__main__":

    part1()
    part2()
