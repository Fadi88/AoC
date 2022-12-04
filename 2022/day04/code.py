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
    total = 0
    for l in open("input.txt"):
        (d1,d2,d3,d4) = list(map(int,re.findall(r"\d+" ,l)))
       
        e1 = range(d1,d2+1)
        e2 = range(d3,d4+1)

        intersection = len(set(e1).intersection(e2))

        if intersection in [len(e1) , len(e2)]:
            total += 1

    print(total)


@profiler
def part2():
    total = 0
    for l in open("input.txt"):
        (d1,d2,d3,d4) = list(map(int,re.findall(r"\d+" ,l)))
       
        e1 = range(d1,d2+1)
        e2 = range(d3,d4+1)

        intersection = len(set(e1).intersection(e2))

        if intersection > 0:
            total += 1

    print(total)


if __name__ == "__main__":

    part1()
    part2()
