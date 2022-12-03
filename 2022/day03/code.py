import time


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print('Method ' + method.__name__ + ' took : ' +
              "{:2.5f}".format(time.time()-t) + ' sec')
        return ret
    return wrapper_method


def getvalue(c):
    if ord(c) < ord('a'):
        return ord(c) - ord('A') + 1 + 26
    else:
        return ord(c) - ord('a') + 1


@profiler
def part1():
    prio = 0

    for l in open("input.txt").read().splitlines():

        h1 = l[:len(l)//2]
        h2 = l[len(l)//2:]
        for c in h1:
            if c in h2:
                prio += getvalue(c)
                break

    print(prio)


@profiler
def part2():
    prio = 0

    items = open("input.txt").read().splitlines()

    for i in range(0, len(items), 3):
        for c in items[i]:
            if items[i+1].count(c) > 0 and items[i+2].count(c) > 0:
                prio += getvalue(c)
                break

    print(prio)


if __name__ == "__main__":

    part1()
    part2()
