import random
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
    pc, a, b = 0, 0, 0
    inst = [l for l in open('input.txt').read().split('\n')]

    executed = []

    while pc not in executed and pc < len(inst):
        i = inst[pc]

        if 'inc' in i:
            if 'a' in i:
                a += 1
            else:
                b += 1
            pc += 1
        elif 'tpl' in i:
            if 'a' in i:
                a *= 3
            else:
                b *= 3
            pc += 1
        elif 'hlf' in i:
            if 'a' in i:
                a //= 2
            else:
                b //= 2
            pc += 1
        elif 'jmp' in i:
            pc += int(i.split()[1])
        elif 'jie' in i:
            if 'a' in i:
                val = a
            else:
                val = b

            if val % 2 == 0:
                pc += int(i.split()[2])
            else:
                pc += 1
        elif 'jio' in i:
            if 'a' in i:
                val = a
            else:
                val = b

            if val == 1:
                pc += int(i.split()[2])
            else:
                pc += 1

    print(b)


@profiler
def part2():
    pc, a, b = 0, 1, 0
    inst = [l for l in open('input.txt').read().split('\n')]

    executed = []

    while pc not in executed and pc < len(inst):
        i = inst[pc]

        if 'inc' in i:
            if 'a' in i:
                a += 1
            else:
                b += 1
            pc += 1
        elif 'tpl' in i:
            if 'a' in i:
                a *= 3
            else:
                b *= 3
            pc += 1
        elif 'hlf' in i:
            if 'a' in i:
                a //= 2
            else:
                b //= 2
            pc += 1
        elif 'jmp' in i:
            pc += int(i.split()[1])
        elif 'jie' in i:
            if 'a' in i:
                val = a
            else:
                val = b

            if val % 2 == 0:
                pc += int(i.split()[2])
            else:
                pc += 1
        elif 'jio' in i:
            if 'a' in i:
                val = a
            else:
                val = b

            if val == 1:
                pc += int(i.split()[2])
            else:
                pc += 1

    print(b)


if __name__ == "__main__":

    pass
    part1()
    part2()
