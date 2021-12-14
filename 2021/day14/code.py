import time
from collections import Counter, defaultdict


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print(
            "Method "
            + method.__name__
            + " took : "
            + "{:2.5f}".format(time.time() - t)
            + " sec"
        )
        return ret

    return wrapper_method


@profiler
def part1():
    p = open("day14/input.txt").read().split("\n\n")

    formula = list(p[0])
    trans = {l.split(" -> ")[0]: l.split(" -> ")[1] for l in p[1].split("\n")}

    for _ in range(10):
        new_formula = []
        for i in range(len(formula) - 1):
            k = "".join([formula[i], formula[i + 1]])
            new_formula += [formula[i], trans[k]]

        new_formula.append(formula[-1])
        formula = new_formula

    freq = sorted(Counter(formula).values())
    print(freq[-1] - freq[0])


@profiler
def part2():
    input = open("day14/input.txt").read().split("\n\n")

    trans = {l.split(" -> ")[0]: l.split(" -> ")[1] for l in input[1].split("\n")}

    pairs = Counter(
        ["".join([input[0][i], input[0][i + 1]]) for i in range(len(input[0]) - 1)]
    )

    for _ in range(40):
        new_pairs = Counter()
        for p in pairs:
            new_pairs[p[0] + trans[p]] += pairs[p]
            new_pairs[trans[p] + p[1]] += pairs[p]

        pairs = new_pairs

    freq = defaultdict(int)

    for p in pairs:
        freq[p[0]] += pairs[p]
        freq[p[1]] += pairs[p]

    # all chars are counted twice except for the first one and last one
    freq[input[0][0]] += 1
    freq[input[0][-1]] += 1

    print((max(freq.values()) - min(freq.values())) // 2)


if __name__ == "__main__":

    part1()
    part2()
