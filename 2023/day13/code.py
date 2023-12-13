# pylint: disable=C0114,C0116,C0301,C0209,W1514

from time import perf_counter


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print("Method " + method.__name__ + " took : " + "{:2.5f}".format(perf_counter() - t) + " sec")
        return ret

    return wrapper_method


def rotate(t):
    return [list(x) for x in zip(*t)]


def get_axis(p):
    ret = None

    for y in range(1, len(p)):
        comp = 0
        sym = 0
        for dy in range(y):
            if 0 <= y - dy - 1 and y + dy < len(p):
                comp += 1
                if p[y - dy - 1] == p[y + dy]:
                    sym += 1
                else:
                    break

        if sym == comp != 0:
            return y
    return ret


@profiler
def part1():
    input = open("day13/input.txt").read().split("\n\n")

    patterns = []
    for i in input:
        patterns.append([list(l.strip()) for l in i.splitlines()])

    total = 0
    for p in patterns:
        y = get_axis(p)
        if y:
            total += 100 * y
        x = get_axis(rotate(p))
        if x:
            total += x

    print(total)


def get_axis_smudged(p):
    ret = None

    for y in range(1, len(p)):
        diff = 0
        for dy in range(y):
            if 0 <= y - dy - 1 and y + dy < len(p):
                diff += sum(r != l for r, l in zip(p[y - dy - 1], p[y + dy]))
            if diff > 1:
                break
        if diff == 1:
            return y
    return ret


@profiler
def part2():
    input = open("day13/input.txt").read().split("\n\n")

    patterns = []
    for i in input:
        patterns.append([list(l.strip()) for l in i.splitlines()])

    total = 0
    for p in patterns:
        y = get_axis_smudged(p)
        if y:
            total += 100 * y
        x = get_axis_smudged(rotate(p))
        if x:
            total += x

    print(total)


if __name__ == "__main__":
    part1()
    part2()
