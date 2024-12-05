# pylint: disable=C0114,C0116,C0301,C0209,W1514

from time import perf_counter
from collections import defaultdict, deque


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print(
            "Method "
            + method.__name__
            + " took : "
            + "{:2.5f}".format(perf_counter() - t)
            + " sec"
        )
        return ret

    return wrapper_method


@profiler
def part1():
    ps = [l.split() for l in open("day05/input.txt").read().split("\n\n")]
    order = defaultdict(list)

    for update_str in ps[0]:
        update = update_str.split("|")
        order[int(update[0])].append(int(update[1]))

    s = 0

    for update_str in ps[1]:
        update = list(map(int, update_str.split(",")))
        ordered = True
        for i, page in enumerate(update):
            if not all(
                page2 in order[page] for i2, page2 in enumerate(update) if i2 > i
            ):
                ordered = False
                break
        s += ordered * update[len(update) // 2]

    print(s)


@profiler
def part2():
    ps = [l.split() for l in open("day05/input.txt").read().split("\n\n")]
    order = defaultdict(list)

    for update_str in ps[0]:
        update = update_str.split("|")
        order[int(update[0])].append(int(update[1]))

    s = 0

    for update_str in ps[1]:
        update = list(map(int, update_str.split(",")))

        if not all(
            page2 in order[page]
            for i, page in enumerate(update)
            for i2, page2 in enumerate(update)
            if i2 > i
        ):

            new_list = []
            to_sort = set(update)
            while to_sort:
                for n in to_sort:
                    if all(n2 in order[n] for n2 in to_sort if n2 != n):
                        new_list.append(n)
                        to_sort.remove(n)
                        break

            s += new_list[len(new_list) // 2]

    print(s)


if __name__ == "__main__":
    part1()
    part2()
