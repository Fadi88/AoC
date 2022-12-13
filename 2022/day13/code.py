import functools
from time import perf_counter
import json


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print('Method ' + method.__name__ + ' took : ' +
              "{:2.5f}".format(perf_counter()-t) + ' sec')
        return ret
    return wrapper_method


def is_in_order(p1, p2):
    for i in range(min(len(p1), len(p2))):
        if isinstance(p1[i], int) and isinstance(p2[i], int):
            if p1[i] == p2[i]:
                continue
            return p1[i] < p2[i]
        elif isinstance(p1[i], int) or isinstance(p2[i], int):
            if isinstance(p1[i], int):
                ret = is_in_order([p1[i]], p2[i])
            else:
                ret = is_in_order(p1[i], [p2[i]])
            if ret is None:
                continue
            return ret
        else:  # both lists
            ret = is_in_order(p1[i], p2[i])
            if ret is None:
                continue
            return ret

    if len(p1) != len(p2):
        return len(p1) < len(p2)


@profiler
def part1():
    index = 1
    total = 0

    for m in open("input.txt").read().split("\n\n"):
        p = m.split("\n")
        if is_in_order(json.loads(p[0]), json.loads(p[1])):
            total += index
        index += 1

    print(total)


@profiler
def part2():

    input = list(map(json.loads, open(
        "input.txt").read().replace("\n\n", "\n").split('\n')))

    p1 = json.loads("[[2]]")
    p2 = json.loads("[[6]]")

    input.append(p1)
    input.append(p2)

    for i in range(len(input) - 1):
        for j in range(0, len(input) - i - 1):
            if not is_in_order(input[j], input[j+1]):
                input[j], input[j+1] = input[j + 1], input[j]

    print((input.index(p1) + 1) * (input.index(p2) + 1))


if __name__ == "__main__":

    part1()
    part2()
