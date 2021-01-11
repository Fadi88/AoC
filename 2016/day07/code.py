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


@profiler
def part1():

    cnt = 0
    with open('input.txt') as f:
        for l in f.read().split('\n'):
            t1 = re.findall(r'\[(\w+)\]', l)
            for t in t1:
                l = l.replace(t, '')

            l = l.replace('[]', ' ')
            t2 = l.split()

            abba_t1 = []
            abba_t2 = []
            for t in t1:
                abba_t1 += [t[i] == t[i+3] and t[i+1] == t[i+2]
                            and not t[i] == t[i+2] for i in range(len(t)-3)]
            for t in t2:
                abba_t2 += [t[i] == t[i+3] and t[i+1] == t[i+2]
                            and not t[i] == t[i+2] for i in range(len(t)-3)]

            if any(abba_t2) and not any(abba_t1):
                cnt += 1

    print(cnt)


@profiler
def part2():

    cnt = 0
    with open('input.txt') as f:
        for l in f.read().split('\n'):
            t1 = re.findall(r'\[(\w+)\]', l)
            for t in t1:
                l = l.replace(t, '')

            l = l.replace('[]', ' ')
            t2 = l.split()

            abba_t1 = []
            abba_t2 = []
            for t in t2:
                abba_t2 += [''.join([t[i], t[i+1], t[i+2]])
                            for i in range(len(t)-2) if t[i] == t[i+2] and not t[i] == t[i+1]]

            for t in abba_t2:
                abba_t1.append(''.join([t[1], t[0], t[1]]) in ''.join(t1))

            if len(abba_t2) > 0 and any(abba_t1):
                cnt += 1

    print(cnt)


if __name__ == "__main__":

    part1()
    part2()
