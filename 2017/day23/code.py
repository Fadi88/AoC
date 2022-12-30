import time
from collections import defaultdict


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print("Method " + method.__name__ + " took : " +
              "{:2.5f}".format(time.time() - t) + " sec")
        return ret

    return wrapper_method


@profiler
def part1():

    reg = defaultdict(int)
    pc = 0
    code = [l for l in open("day23/input.txt").read().splitlines()]

    mul_used = 0

    while pc < len(code):
        ops = code[pc].split()

        if ops[2].isnumeric() or '-' in ops[2]:
            val = int(ops[2])
        else:
            val = reg[ops[2]]

        if ops[0] == "set":
            reg[ops[1]] = val
            pc += 1
        elif ops[0] == "sub":
            reg[ops[1]] -= val
            pc += 1
        elif ops[0] == "mul":
            reg[ops[1]] *= val
            pc += 1
            mul_used += 1
        elif ops[0] == "jnz":
            if ops[1].isnumeric():
                check = int(ops[1])
            else:
                check = reg[ops[1]]

            if check != 0:
                pc += val
            else:
                pc += 1
    print(mul_used)


@profiler
def part2():

    h = 0
    code = [l for l in open("day23/input.txt").read().splitlines()]

    step = -int(code[30].split()[2])

    b = int(code[0].split()[2]) * \
        int(code[4].split()[2]) - int(code[5].split()[2])
    c = b - int(code[7].split()[2])

    e_init = int(code[10].split()[2])

    for x in range(b, c+1, step):
        for e in range(e_init, x):
            if x % e == 0:  # f
                h += 1
                break

    print(h)


if __name__ == "__main__":

    part1()
    part2()
