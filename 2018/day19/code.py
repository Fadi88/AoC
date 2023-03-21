import time
import re
from functools import reduce


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print("Method " + method.__name__ + " took : " +
              "{:2.5f}".format(time.time() - t) + " sec")
        return ret

    return wrapper_method

@profiler
def part_1():
    data = open("day19/input.txt").read().splitlines()
    
    ip_reg = int(data[0].split()[1])
    reg = [0] * 6
    del data[0]

    while reg[ip_reg] in range(len(data)):

        current = data[reg[ip_reg]]
        a, b , c = list(map(int,re.findall(r"\d+" , current)))
        
        if "seti" in current:
            reg[c] = a
        elif "setr" in current:
            reg[c] = reg[a]
        elif "addr" in current:
            reg[c] = reg[a] + reg[b]
        elif "addi" in current:
            reg[c] = reg[a] + b
        elif "mulr" in current:
            reg[c] = reg[a] * reg[b]
        elif "muli" in current:
            reg[c] = reg[a] * b
        elif "eqrr" in current:
            reg[c] = int(reg[a] == reg[b])
        elif "gtrr" in current:
            reg[c] = int(reg[a] > reg[b])
        else :
            raise Exception("Not impelmented" , current)

        reg[ip_reg] += 1
    print(reg[0])

@profiler
def part_2():
    data = open("day19/input.txt").read().splitlines()
    
    ip_reg = int(data[0].split()[1])
    reg = [0] * 6
    reg[0] = 1
    del data[0]
    
    cycles = 0
    target_reg = int(data[17].split()[3])

    while reg[ip_reg] in range(len(data)) and cycles < 20:

        cycles += 1
        current = data[reg[ip_reg]]
        a, b , c = list(map(int,re.findall(r"\d+" , current)))
        
        if "seti" in current:
            reg[c] = a
        elif "setr" in current:
            reg[c] = reg[a]
        elif "addr" in current:
            reg[c] = reg[a] + reg[b]
        elif "addi" in current:
            reg[c] = reg[a] + b
        elif "mulr" in current:
            reg[c] = reg[a] * reg[b]
        elif "muli" in current:
            reg[c] = reg[a] * b
        elif "eqrr" in current:
            reg[c] = int(reg[a] == reg[b])
        elif "gtrr" in current:
            reg[c] = int(reg[a] > reg[b])
        else :
            raise Exception("Not impelmented" , current)

        reg[ip_reg] += 1
    
    n = reg[target_reg]
    print(
        sum(
            reduce(
                list.__add__,
                ([i, n // i] for i in range(1, int(n**0.5) + 1) if n % i == 0),
            )
        )
    )


if __name__ == "__main__":

    part_1()
    part_2()
