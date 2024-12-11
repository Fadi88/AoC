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


@profiler
def part_1():
    with open(input_file) as f:
        l = list(map(int, f.read().split()))

    for _ in range(25):
        new_l = list()
        for s in l:
            if s == 0:
                new_l.append(1)
            elif len(str(s)) % 2 == 0:
                num = str(s)
                new_l.append(int(str(num[:len(num)//2])))
                new_l.append(int(str(num[len(num)//2:])))
            else:
                new_l.append(s*2024)
        l = new_l

    print(len(l))


@profiler
def part_2():
    with open(input_file) as f:
        l = list(map(int, f.read().split()))

    # l = [125,17]
    l = Counter(l)

    for _ in range(75):
        new_l = Counter()
        for s in l:
            if s == 0:
                new_l[1] += l[s]
            elif len(str(s)) % 2 == 0:
                num = str(s)
                n1 = int(str(num[:len(num)//2]))
                n2 = int(str(num[len(num)//2:]))
                new_l[n1] += l[s]
                new_l[n2] += l[s]

            else:
                new_l[s*2024] += l[s]

        l = new_l

    print(sum(l.values()))


if __name__ == "__main__":
    part_1()
    part_2()
