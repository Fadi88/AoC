import time
from itertools import tee


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print('Method ' + method.__name__ + ' took : ' +
              "{:2.5f}".format(time.time()-t) + ' sec')
        return ret
    return wrapper_method


def comp(inst, val):

    reg = [0] * 4
    reg_map = {'a': 0, 'b': 1, 'c': 2, 'd': 3}
    pc = 0

    reg[0] = val

    out = []

    while pc < len(inst):

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
            if val != 0:
                pc += int(p[2])
            else:
                pc += 1

        elif 'out' in inst[pc]:
            p = inst[pc].split()
            if p[1] in reg_map.keys():
                out.append(str(reg[reg_map[p[1]]]))
            else:
                out.append(str(p[1]))
            pc += 1

            if len(out) == 10:
                return ''.join(out)


@profiler
def part1():

    inst = []

    for l in open('input.txt').read().split('\n'):
        inst.append(l)

    seed = 0
    while True:
        ret = comp(inst, seed)
        if ret == '0101010101' or ret == '1010101010':
            break

        seed += 1

    print(seed)


if __name__ == "__main__":

    part1()
