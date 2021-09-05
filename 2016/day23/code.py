import time
import re
from collections import deque


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
    reg_map = {'a': 0, 'b': 1, 'c': 2, 'd': 3}

    reg[reg_map['a']] = 7
    pc = 0

    while pc < len(inst):
        #print(reg, pc, inst[pc])
        if 'inc' in inst[pc]:
            reg[reg_map[inst[pc].split()[1]]] += 1
            pc += 1

        elif 'dec' in inst[pc]:
            reg[reg_map[inst[pc].split()[1]]] -= 1
            pc += 1

        elif 'cpy' in inst[pc]:
            p = inst[pc].split()
            if p[1] in reg_map.keys():
                val = reg[reg_map[p[1]]]
            else:
                val = int(p[1])
            reg[reg_map[p[2]]] = val
            pc += 1

        elif 'jnz' in inst[pc]:
            p = inst[pc].split()
            if p[1] in reg_map.keys():
                val = reg[reg_map[p[1]]]
            else:
                val = int(p[1])
            if p[2] in reg_map.keys():
                off = reg[reg_map[p[2]]]
            else:
                off = int(p[2])
            if val != 0:
                pc += off
            else:
                pc += 1
        elif 'tgl' in inst[pc]:
            p = inst[pc].split()
            new_idx = pc + reg[reg_map[p[1]]]

            if new_idx >= len(inst):
                pc += 1
                continue

            n_p = inst[new_idx].split()

            if len(n_p) == 2:
                if 'inc' in inst[new_idx]:
                    inst[new_idx] = inst[new_idx].replace('inc', 'dec')
                else:
                    inst[new_idx] = inst[new_idx].replace(n_p[0], 'inc')

            elif len(n_p) == 3:
                if 'jnz' in inst[new_idx]:
                    inst[new_idx] = inst[new_idx].replace('jnz', 'cpy')
                else:
                    inst[new_idx] = inst[new_idx].replace(n_p[0], 'jnz')

            pc += 1

    print(reg[0])


@profiler
def part2():

    inst = []

    for l in open('input.txt').read().split('\n'):
        inst.append(l)

    reg = [0] * 4
    reg_map = {'a': 0, 'b': 1, 'c': 2, 'd': 3}

    reg[reg_map['a']] = 12
    pc = 0

    while pc < len(inst):
        if pc == 4:
            reg[0] = reg[1] * reg[3]
            reg[3] = 0
            pc += 6
        elif 'inc' in inst[pc]:
            reg[reg_map[inst[pc].split()[1]]] += 1
            pc += 1
        elif 'dec' in inst[pc]:
            reg[reg_map[inst[pc].split()[1]]] -= 1
            pc += 1
        elif 'cpy' in inst[pc]:
            p = inst[pc].split()
            if p[1] in reg_map.keys():
                val = reg[reg_map[p[1]]]
            else:
                val = int(p[1])
            reg[reg_map[p[2]]] = val
            pc += 1

        elif 'jnz' in inst[pc]:
            p = inst[pc].split()
            if p[1] in reg_map.keys():
                val = reg[reg_map[p[1]]]
            else:
                val = int(p[1])
            if p[2] in reg_map.keys():
                off = reg[reg_map[p[2]]]
            else:
                off = int(p[2])
            if val != 0:
                pc += off
            else:
                pc += 1
        elif 'tgl' in inst[pc]:
            p = inst[pc].split()
            new_idx = pc + reg[reg_map[p[1]]]

            if new_idx >= len(inst):
                pc += 1
                continue

            n_p = inst[new_idx].split()

            if len(n_p) == 2:
                if 'inc' in inst[new_idx]:
                    inst[new_idx] = inst[new_idx].replace('inc', 'dec')
                else:
                    inst[new_idx] = inst[new_idx].replace(n_p[0], 'inc')

            elif len(n_p) == 3:
                if 'jnz' in inst[new_idx]:
                    inst[new_idx] = inst[new_idx].replace('jnz', 'cpy')
                else:
                    inst[new_idx] = inst[new_idx].replace(n_p[0], 'jnz')

            pc += 1

    print(reg[0])


if __name__ == "__main__":

    part1()
    part2()
