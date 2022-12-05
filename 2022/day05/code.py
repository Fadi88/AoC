from collections import defaultdict
from time import perf_counter


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print('Method ' + method.__name__ + ' took : ' +
              "{:2.5f}".format(perf_counter()-t) + ' sec')
        return ret
    return wrapper_method


@profiler
def part1():
    cargo = defaultdict(list)
    parts = open("input.txt").read().split("\n\n")
    config = parts[0].split('\n')

    for l in config[:-1]:
        for i, c in enumerate(l):
            if c.isalpha():
                cargo[config[-1][i]].insert(0, c)

    for l in parts[1].split("\n"):
        move = list(l.replace("move", "").replace(
            "to", "").replace("from", "").split())

        cargo[move[2]] += cargo[move[1]][-int(move[0]):][::-1]
        del cargo[move[1]][-int(move[0]):]

    print("".join([cargo[str(i)][-1] for i in range(1, 10)]))


@profiler
def part2():
    cargo = defaultdict(list)
    parts = open("input.txt").read().split("\n\n")
    config = parts[0].split('\n')

    for l in config[:-1]:
        for i, c in enumerate(l):
            if c.isalpha():
                cargo[config[-1][i]].insert(0, c)

    for l in parts[1].split("\n"):
        move = list(l.replace("move", "").replace(
            "to", "").replace("from", "").split())

        cargo[move[2]] += cargo[move[1]][-int(move[0]):]
        del cargo[move[1]][-int(move[0]):]

    print("".join([cargo[str(i)][-1] for i in range(1, 10)]))


if __name__ == "__main__":

    part1()
    part2()
