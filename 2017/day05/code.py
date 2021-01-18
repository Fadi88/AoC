import time
import math


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        method(*arg, **kw)
        print('Method ' + method.__name__ + ' took : ' +
              "{:2.5f}".format(time.time()-t) + ' sec')
    return wrapper_method


@profiler
def part1():

    inp = [* map(int, open('input.txt').read().strip().split('\n'))]

    pc = 0
    steps = 0

    while pc < len(inp):
        steps += 1

        inp[pc] += 1
        pc += inp[pc] - 1

    print(steps)


@profiler
def part2():

    inp = [* map(int, open('input.txt').read().strip().split('\n'))]

    pc = 0
    steps = 0

    while pc < len(inp):
        steps += 1

        if inp[pc] >= 3:
            inp[pc] -= 1
            pc += inp[pc] + 1
        else:
            inp[pc] += 1
            pc += inp[pc] - 1

    print(steps)


if __name__ == "__main__":

    part1()
    part2()
