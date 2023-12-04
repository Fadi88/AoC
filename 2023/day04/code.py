from time import perf_counter
from collections import defaultdict


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
    total = 0

    for l in open("day04/input.txt"):
        ticket = l.split(":")[1].split("|")

        winning = set(map(int,ticket[0].split()))
        nums = set(map(int,ticket[1].split()))

        total += int(2 ** (len(winning.intersection(nums)) - 1))

    print(total)


@profiler
def part2():

    ticket_count = defaultdict(int)

    for card,l in enumerate(open("day04/input.txt")):
        ticket = l.split(":")[1].split("|")

        ticket_count[card+1] += 1

        winning = set(map(int,ticket[0].split()))
        nums = set(map(int,ticket[1].split()))

        for n in range(len(winning.intersection(nums))):
            ticket_count[card + 2 + n] += ticket_count[card+1]

    print(sum(ticket_count.values()))


if __name__ == "__main__":

    part1()
    part2()
