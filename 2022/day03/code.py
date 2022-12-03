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
    total = 0

    for l in open("input.txt").read().splitlines():
        for c in l[:len(l)//2]:
            if c in l[len(l)//2:]:
                total += getvalue(c)
                break

    print(total)


@profiler
def part2():
    total = 0

    items = open("input.txt").read().splitlines()

    for i in range(0, len(items), 3):
        for c in items[i]:
            if c in items[i+1] and c in items[i+2]:
                total += getvalue(c)
                break

    print(total)


if __name__ == "__main__":

    part1()
    part2()
