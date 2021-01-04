import time,os,re
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
    with open('input.txt', 'r') as f:
        print(sum([len(l.strip()) - len(eval(l.strip())) for l in f ]))

@profiler
def part2():
    with open('input.txt', 'r') as f:
        print(sum([2 + l.count('\\') + l.count(r'"') for l in f]))

if __name__ == "__main__":

    part1()
    part2()
