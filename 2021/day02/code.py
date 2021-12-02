import time
import re


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

    pos = 0

    for l in open('input.txt'):
        ds = int(re.findall(r'\d+', l)[0])
        if "up" in l:
            pos -= ds * 1j
        elif "down" in l:
            pos += ds * 1j
        elif "forward" in l:
            pos += ds

    print("part 1 :", int(pos.real * pos.imag))


@profiler
def part2():

    pos = 0
    aim = 0

    for l in open('input.txt'):
        ds = int(re.findall(r'\d+', l)[0])
        if "up" in l:
            aim -= ds
        elif "down" in l:
            aim += ds
        elif "forward" in l:
            pos += ds
            pos += (aim * ds * 1j)

    print("part 2 :", int(pos.real * pos.imag))


if __name__ == "__main__":

    part1()
    part2()
