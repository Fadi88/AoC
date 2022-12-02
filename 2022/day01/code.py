import time


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
    cals = [sum([int(c) for c in l.split()])
            for l in open("input.txt").read().split("\n\n")]
    print(max(cals))


@profiler
def part2():
    cals = [sum([int(c) for c in l.split()])
            for l in open("input.txt").read().split("\n\n")]
    cals.sort()
    print(sum(cals[-3:]))


if __name__ == "__main__":

    part1()
    part2()
