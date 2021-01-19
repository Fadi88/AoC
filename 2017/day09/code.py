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

    inp = open('input.txt').read().strip()

    #inp = '{{<a},{<a},{<a},{<ab>}}'
    open_groups = 0
    score = 0
    open_garbage = 0

    while inp.count('!!') > 0:
        inp = inp.replace('!!' , '')

    for i in range(len(inp)):

        c = inp[i]
        if i > 0 and inp[i-1] == '!' : continue

        if c == '<':
            open_garbage += 1
        elif c == '>':
            open_garbage = 0
        if c == '{' and open_garbage == 0:
            open_groups += 1
            score += open_groups
        elif c == '}' and open_garbage == 0:
            open_groups -= 1

        assert open_groups >= 0


    print(score)

        

@profiler
def part2():

    inp = open('input.txt').read().strip()

    score = 0
    open_garbage = 0

    while inp.count('!!') > 0:
        inp = inp.replace('!!' , '')

    for i in range(len(inp)):

        c = inp[i]
        if i > 0 and inp[i-1] == '!' : continue

        if c == '<' and open_garbage == 0:
            open_garbage = 1
        elif c == '>' and open_garbage == 1:
            open_garbage = 0
        
        elif open_garbage == 1 and c != '!':
            score += 1
            #print(c,end='')

    print(score)


if __name__ == "__main__":

    part1()
    part2()
