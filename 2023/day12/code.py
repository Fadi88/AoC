# pylint: disable=C0114,C0116,C0301,C0209,W1514

from time import perf_counter
from functools import cache


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print("Method " + method.__name__ + " took : " + "{:2.5f}".format(perf_counter() - t) + " sec")
        return ret

    return wrapper_method


@cache
def get_comb(pattern, nums):
    if len(pattern) == 0:
        return len(nums) == 0

    match pattern[0]:
        case "?":
            return get_comb(pattern.replace("?", ".", 1), nums) + get_comb(pattern.replace("?", "#", 1), nums)
        case ".":
            return get_comb(pattern.strip("."), nums)
        case "#":
            if (
                len(nums) == 0
                or len(pattern) < sum(nums)
                or len(pattern) < nums[0]
                or pattern[: nums[0]].count(".") > 0
                or (len(nums) > 1 and len(pattern) < nums[0] + 1)
                or (len(nums) > 1 and pattern[nums[0]] == "#")
            ):
                return 0
            # nasty nasty nasty bug for the last spring :/ 
            return get_comb(pattern[nums[0] + (len(nums) > 1) :], nums[1:])


@profiler
def part1():
    total = 0

    for l in open("day12/input.txt"):
        pattern = l.split()[0]
        nums = tuple(map(int, l.split()[1].split(",")))

        total += get_comb(pattern, nums)

    print(total)


@profiler
def part2():
    total = 0

    for l in open("day12/input.txt"):
        pattern = l.split()[0]
        nums = tuple(map(int, l.split()[1].split(",")))

        total += get_comb("?".join([pattern] * 5), nums * 5)

    print(total)


if __name__ == "__main__":
    part1()
    part2()