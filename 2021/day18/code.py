import time
import re
from itertools import permutations


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


class Depth:
    def __init__(self, exp) -> None:
        self.exp = "" + exp

    def __call__(self, pairs):

        depth = []
        for p in pairs[::-1]:
            loc = self.exp.rfind(p)
            depth.append((self.exp[:loc].count("[") - self.exp[:loc].count("]"), loc))
            self.exp = self.exp[:loc] + self.exp[loc + len(p) :]

        return depth[::-1]


def reduce_exp(exp):
    while True:
        depth_obj = Depth(exp)

        gt_10 = re.findall(r"(\d{2,})", exp)
        pairs = re.findall(r"(\[\d+,\d+\])", exp)

        depth = depth_obj(pairs)

        if any(map(lambda x: x[0] > 3, depth)):
            loc_depth, deep_pair = next(
                (v[1], pairs[i]) for i, v in enumerate(depth) if v[0] > 3
            )

            left_exp = exp[:loc_depth]
            right_exp = exp[loc_depth + len(deep_pair) :]

            ps = list(map(int, deep_pair[1:-1].split(",")))

            if re.match(r".*\d+.*", left_exp):
                l_d = re.findall(r"(\d+)", left_exp)[-1]
                l_loc = left_exp.rfind(l_d)
                left_exp = (
                    left_exp[:l_loc]
                    + str(int((l_d)) + ps[0])
                    + left_exp[l_loc + len(l_d) :]
                )

            if re.match(r".*\d+.*", right_exp):
                r_d = re.findall(r"(\d+)", right_exp)
                right_exp = right_exp.replace(r_d[0], str(int((r_d[0])) + ps[1]), 1)

            exp = left_exp + "0" + right_exp

        elif len(gt_10) > 0:
            tmp = int(gt_10[0])
            new_st = "[" + str(tmp // 2) + "," + str(tmp // 2 + tmp % 2) + "]"
            exp = exp.replace(gt_10[0], new_st, 1)

        else:
            break

    return exp


def magnitude(exp):

    while True:
        pairs = re.findall(r"(\[\d+,\d+\])", exp)
        if len(pairs) == 0:
            break
        for p in pairs:
            ps = list(map(int, p[1:-1].split(",")))
            exp = exp.replace(p, str(3 * ps[0] + 2 * ps[1]))
    return int(exp)


@profiler
def part1():
    exp = ""
    for l in open("day18/input.txt"):
        l = l.strip()
        if len(exp) == 0:
            exp += l
        else:
            exp = reduce_exp("[" + exp + "," + l + "]")

    print(magnitude(exp))


@profiler
def part2():
    input = open("day18/input.txt").read().split("\n")
    print(
        max(
            [
                magnitude(reduce_exp("[" + p[0] + "," + p[1] + "]"))
                for p in permutations(input, 2)
            ]
        )
    )


if __name__ == "__main__":

    part1()
    part2()
