from time import perf_counter
import math


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print('Method ' + method.__name__ + ' took : ' +
              "{:2.5f}".format(perf_counter()-t) + ' sec')
        return ret
    return wrapper_method


class Monkey:
    def __init__(self, m):
        for l in m.splitlines():
            if "Starting items:" in l:
                self.items = list(map(int, l.strip().replace(
                    "Starting items: ", "").replace(",", "").split(" ")))
            elif "Operation:" in l:
                p = l.split()
                self.operation = (p[-2], p[-1])
            elif "Test:" in l:
                self.test = int(l.split()[-1])
            elif "If true:" in l:
                self.if_true = int(l.split()[-1])
            elif "If false:" in l:
                self.if_false = int(l.split()[-1])

        self.activity = 0

    def round(self):
        ret = []
        for i in self.items:
            self.activity += 1
            new_level = eval(
                "i" + self.operation[0] + self.operation[1].replace("old", "i"))//3
            ret.append((self.if_true if new_level %
                       self.test == 0 else self.if_false, new_level))
        self.items = []

        return ret

    def round_2(self):
        ret = []
        for i in self.items:
            self.activity += 1
            new_level = eval(
                "i" + self.operation[0] + self.operation[1].replace("old", "i"))
            ret.append((self.if_true if new_level %
                       self.test == 0 else self.if_false, new_level))
        self.items = []

        return ret


@profiler
def part1():
    monkeys = []

    for m in open("input.txt").read().split("\n\n"):
        monkeys.append(Monkey(m))

    for _ in range(20):
        for m in range(len(monkeys)):
            tmp = monkeys[m].round()
            for i in tmp:
                monkeys[i[0]].items.append(i[1])
    monkeys.sort(key=lambda x: x.activity, reverse=True)

    print(monkeys[0].activity * monkeys[1].activity)


@profiler
def part2():
    monkeys = []

    for m in open("input.txt").read().split("\n\n"):
        monkeys.append(Monkey(m))

    divisor = math.prod([m.test for m in monkeys])

    for _ in range(10000):
        for m in range(len(monkeys)):
            tmp = monkeys[m].round_2()
            for i in tmp:
                monkeys[i[0]].items.append(i[1] % divisor)

    monkeys.sort(key=lambda x: x.activity, reverse=True)

    print(monkeys[0].activity * monkeys[1].activity)


if __name__ == "__main__":

    part1()
    part2()
