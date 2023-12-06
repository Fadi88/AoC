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
    input = []
    for l in open("day06/input.txt"):
        input.append(list(map(int,l.split()[1:])))

    total = 1
    for tt,d in zip(input[0],input[1]):
        wins = 0
        for t in range(tt+1):
            if (tt-t)*t > d:
                wins += 1
        total *= wins
    print(total)


@profiler
def part2():
    input = []
    for l in open("day06/input.txt"):
        input.append(int("".join(l.split()[1:])))

    wins = 0
    tt = input[0]
    d = input[1]
    for t in range(tt+1):
        if (tt-t)*t > d:
            wins += 1
    print(wins)


if __name__ == "__main__":

    part1()
    part2()
