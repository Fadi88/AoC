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

    inst = []

    for l in open('input.txt').read().split('\n'):
        inst.append(l)

    reg = [0] * 4
    reg_map = {'a' : 0 , 'b' : 1 , 'c' : 2 , 'd' : 3}
    pc = 0


    while pc < len(inst):

        if 'inc' in inst[pc]:
            reg[reg_map[inst[pc].split()[1]]] += 1
            pc += 1

        elif 'dec' in inst[pc]:
            reg[reg_map[inst[pc].split()[1]]] -= 1
            pc += 1

        elif 'cpy'  in inst[pc]:
            p = inst[pc].split()
            if p[1] in reg_map.keys():
                val = reg[reg_map[p[1]]]
            else :
                val = int(p[1])
            reg[reg_map[p[2]]] = val
            pc += 1

        elif 'jnz' in inst[pc]:
            p = inst[pc].split()
            if p[1] in reg_map.keys():
                val = reg[reg_map[p[1]]]
            else :
                val = int(p[1])
            if val != 0:
                pc += int(p[2])
            else:
                pc += 1

    print(reg[0])




@profiler
def part2():

    inst = []

    for l in open('input.txt').read().split('\n'):
        inst.append(l)

    reg = [0] * 4
    reg_map = {'a' : 0 , 'b' : 1 , 'c' : 2 , 'd' : 3}
    pc = 0

    reg[2] = 1

    while pc < len(inst):

        if 'inc' in inst[pc]:
            reg[reg_map[inst[pc].split()[1]]] += 1
            pc += 1

        elif 'dec' in inst[pc]:
            reg[reg_map[inst[pc].split()[1]]] -= 1
            pc += 1

        elif 'cpy'  in inst[pc]:
            p = inst[pc].split()
            if p[1] in reg_map.keys():
                val = reg[reg_map[p[1]]]
            else :
                val = int(p[1])
            reg[reg_map[p[2]]] = val
            pc += 1

        elif 'jnz' in inst[pc]:
            p = inst[pc].split()
            if p[1] in reg_map.keys():
                val = reg[reg_map[p[1]]]
            else :
                val = int(p[1])
            if val != 0:
                pc += int(p[2])
            else:
                pc += 1

    print(reg[0])



if __name__ == "__main__":

    part1()
    part2()
