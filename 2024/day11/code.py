# pylint: disable=C0114,C0116,C0301,C0209,W1514,C0414,C0200

from time import time as perf_counter
from typing import Any
import os
from collections import Counter

input_file = os.path.join(os.path.dirname(__file__), "input.txt")
# input_file = os.path.join(os.path.dirname(__file__), "test.txt")


def profiler(method):
    def wrapper_method(*args: Any, **kwargs: Any) -> Any:
        t = perf_counter()
        ret = method(*args, **kwargs)
        print(f"Method {method.__name__} took : {perf_counter() - t:.3f} sec")
        return ret

    return wrapper_method


def count_after_blinking(l_cnt, n):
    l_cnt = Counter(l_cnt)

    for _ in range(n):
        new_l = Counter()
        for s in l_cnt:
            if s == 0:
                new_l[1] += l_cnt[s]
            elif len(str(s)) % 2 == 0:
                num = str(s)
                n1 = int(str(num[:len(num)//2]))
                n2 = int(str(num[len(num)//2:]))
                new_l[n1] += l_cnt[s]
                new_l[n2] += l_cnt[s]

            else:
                new_l[s*2024] += l_cnt[s]

        l_cnt = new_l

    return sum(l_cnt.values())


@profiler
def part_1():
    with open(input_file) as f:
        l = list(map(int, f.read().split()))

    print(count_after_blinking(l, 25))


@profiler
def part_2():
    with open(input_file) as f:
        l = list(map(int, f.read().split()))

    print(count_after_blinking(l, 75))


if __name__ == "__main__":
    part_1()
    part_2()
