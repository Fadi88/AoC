from time import perf_counter
import re


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print('Method ' + method.__name__ + ' took : ' +
              "{:2.5f}".format(perf_counter()-t) + ' sec')
        return ret
    return wrapper_method


def get_val(monkeys, key):
    if monkeys[key].isnumeric():
        return int(monkeys[key])

    p = monkeys[key].split()
    return eval(str(get_val(monkeys, p[0])) + p[1] + str(get_val(monkeys, p[2])))


@profiler
def part1():
    monkeys = {}
    for l in open("input.txt").read().splitlines():
        p = l.split(":")
        monkeys[p[0]] = p[1].strip()

    print(int(get_val(monkeys, "root")))


def simplify(expr):
    while True:
        par = re.findall(r"\(-?\d+[*-\\+]-?\d+\)", expr)
        if len(par) == 0:
            return expr

        for e in par:
            expr = expr.replace(e, str(int(eval(e))))


def get_eq(monkeys, key):
    if key == "humn":
        return key

    if monkeys[key].isnumeric():
        return monkeys[key]

    p = monkeys[key].split()

    if key == "root":
        lhs = str(get_eq(monkeys, p[0]))
        rhs = str(get_eq(monkeys, p[2]))

        if "humn" not in lhs:
            lhs = str(int(eval(lhs)))
        else:
            rhs = str(int(eval(rhs)))
        return "(" + rhs + ") = (" + lhs + ")"
    return "(" + str(get_eq(monkeys, p[0])) + p[1] + str(get_eq(monkeys, p[2])) + ")"


@profiler
def part2():
    monkeys = {}
    for l in open("input.txt").read().splitlines():
        p = l.split(":")
        monkeys[p[0]] = p[1].strip()

    eq = get_eq(monkeys, "root").split("=")

    rhs, lhs = eq if "humn" in eq[0] else eq[::-1]
    rhs, lhs = simplify(rhs), int(lhs[1:-2])

    r = [0, 1e15]

    while True:
        mid = sum(r)//2

        if eval(rhs.replace("humn", str(mid))) < lhs:
            r[1] = mid
        elif eval(rhs.replace("humn", str(mid))) > lhs:
            r[0] = mid
        else:
            print(int(mid))
            break


if __name__ == "__main__":

    part1()
    part2()
