# pylint: disable=C0114,C0116,C0301,C0209,W1514

from time import perf_counter
from copy import deepcopy


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print("Method " + method.__name__ + " took : " + "{:2.5f}".format(perf_counter() - t) + " sec")
        return ret

    return wrapper_method


@profiler
def part1():
    ps = open("day19/input.txt").read().split("\n\n")

    rules = {}

    for l in ps[0].splitlines():
        p = l.split("{")
        rules[p[0]] = p[1][:-1]

    A = 0
    for p in ps[1].splitlines():
        state = "in"
        vals = {}
        for c in p[1:-1].split(","):
            vals[c.split("=")[0]] = int(c.split("=")[1])
        while state not in "AR":
            current_cond = rules[state].split(",")
            for pred in current_cond:
                if ":" in pred:
                    evs = pred.split(":")
                    if eval('vals["' + evs[0][0] + '"]' + "".join(evs[0][1:])):
                        state = evs[1]
                        break
                else:
                    state = pred

            if state == "A":
                A += sum(vals.values())
                break
            elif state == "R":
                break

    print(A)


def get_combs(state, rules, ranges={"x": (1, 4000), "m": (1, 4000), "a": (1, 4000), "s": (1, 4000)}):
    if state == "R":
        return 0
    elif state == "A":
        x_s = ranges["x"]
        m_s = ranges["m"]
        a_s = ranges["a"]
        s_s = ranges["s"]

        return (x_s[1] - x_s[0] + 1) * (m_s[1] - m_s[0] + 1) * (a_s[1] - a_s[0] + 1) * (s_s[1] - s_s[0] + 1)

    total = 0
    for pred in rules[state].split(","):
        if not ":" in pred:
            total += get_combs(pred, rules, ranges)
        else:
            p = pred.split(":")
            new_range = deepcopy(ranges)

            new_val = int(p[0][2:])
            c_range = ranges[p[0][0]]

            if c_range[0] < new_val < c_range[1]:
                if p[0][1] == "<":
                    new_range[p[0][0]] = (c_range[0], new_val - 1)
                    ranges[p[0][0]] = (new_val, c_range[1])
                else:
                    new_range[p[0][0]] = (new_val + 1, c_range[1])
                    ranges[p[0][0]] = (c_range[0], new_val)
                total += get_combs(p[1], rules, new_range)
    return total


@profiler
def part2():
    ps = open("day19/input.txt").read().split("\n\n")

    rules = {}

    for l in ps[0].splitlines():
        p = l.split("{")
        rules[p[0]] = p[1][:-1]

    print(get_combs("in", rules))


if __name__ == "__main__":
    part1()
    part2()