import time
import re
from copy import deepcopy

def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print("Method " + method.__name__ + " took : " +
              "{:2.5f}".format(time.time() - t) + " sec")
        return ret

    return wrapper_method

def extract(st):
    return list(map(int,re.findall(r"\d+" , st)))

def addr(reg,a,b,c):
    reg[c] = reg[a] + reg[b]

def addi(reg,a,b,c):
    reg[c] = reg[a] + b

def mulr(reg,a,b,c):
    reg[c] = reg[a] * reg[b]

def muli(reg,a,b,c):
    reg[c] = reg[a] * b

def banr(reg,a,b,c):
    reg[c] = reg[a] & reg[b]

def bani(reg,a,b,c):
    reg[c] = reg[a] & b

def borr(reg,a,b,c):
    reg[c] = reg[a] | reg[b]

def bori(reg,a,b,c):
    reg[c] = reg[a] | b

def setr(reg,a,b,c):
    reg[c] = reg[a]

def seti(reg,a,b,c):
    reg[c] = a

def gtir(reg,a,b,c):
    reg[c] = int(a > reg[b])

def gtri(reg,a,b,c):
    reg[c] = int(reg[a] > b)

def gtrr(reg,a,b,c):
    reg[c] = int(reg[a] > reg[b])

def eqir(reg,a,b,c):
    reg[c] = int(a == reg[b])

def eqri(reg,a,b,c):
    reg[c] = int(reg[a] == b)

def eqrr(reg,a,b,c):
    reg[c] = int(reg[a] == reg[b])

ops = [
    addr, addi, mulr, muli, banr, bani, borr, bori,
    setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr
]

@profiler
def part_1():
    manual = open("day16/input.txt").read().split("\n\n\n")

    total = 0

    for entry in manual[0].split("\n\n"):
        b, op , af = list(map(extract,entry.splitlines()))

        possible = 0

        for fn in ops:
            tmp = deepcopy(b)
            fn(tmp, op[1], op[2] , op[3])

            if tmp == af:
                possible += 1

                if possible == 3:
                    total += 1
                    break

    print(total)

def print_sz(mapping):
    for m in mapping:
        print( str(m) + " : " + str(len(mapping[m])) , end=", ")
    print()


@profiler
def part_2():
    manual = open("day16/input.txt").read().split("\n\n\n\n")

    mapping = { i : set(ops) for i in range(16)}

    for entry in manual[0].split("\n\n"):
        b, op , af = list(map(extract,entry.splitlines()))

        for fn in deepcopy(mapping[op[0]]):
            tmp = deepcopy(b)
            fn(tmp, op[1], op[2] , op[3])

            if tmp != af:
                mapping[op[0]].remove(fn)

    confirmed = {}

    while len(confirmed) < len(ops):
        for m in mapping:
            if len(mapping[m]) == 1 and m not in confirmed:
                confirmed[m] = mapping[m].pop()

        for fn in confirmed.values():
            for m in mapping:
                if fn in mapping[m]:
                    mapping[m].remove(fn)
    reg = [0] * 4

    for code in manual[1].splitlines():
        op = extract(code)
        confirmed[op[0]](reg, op[1], op[2], op[3])
    print(reg[0])



if __name__ == "__main__":

    part_1()
    part_2()
