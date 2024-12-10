# pylint: disable=C0114,C0116,C0301,C0209,W1514,C0414,C0200

import sys
from time import time as perf_counter
from typing import Any
import os

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
        i = f.read()


@profiler
def part_2():
    with open(input_file) as f:
        i = f.read().strip()


if __name__ == "__main__":
    part_1()
    part_2()


def pr(s):
    print(s)


sys.setrecursionlimit(10**6)
infile = input_file
p1 = 0
p2 = 0
D = open(infile).read().strip()


@profiler
def solve(part2):
    A = deque([])
    SPACE = deque([])
    file_id = 0
    FINAL = []
    pos = 0
    for i, c in enumerate(D):
        if i % 2 == 0:
            if part2:
                A.append((pos, int(c), file_id))
            for i in range(int(c)):
                FINAL.append(file_id)
                if not part2:
                    A.append((pos, 1, file_id))
                pos += 1
            file_id += 1
        else:
            SPACE.append((pos, int(c)))
            for i in range(int(c)):
                FINAL.append(None)
                pos += 1

    for (pos, sz, file_id) in reversed(A):
        for space_i, (space_pos, space_sz) in enumerate(SPACE):
            if space_pos < pos and sz <= space_sz:
                for i in range(sz):
                    assert FINAL[pos+i] == file_id, f'{FINAL[pos+i]=}'
                    FINAL[pos+i] = None
                    FINAL[space_pos+i] = file_id
                SPACE[space_i] = (space_pos + sz, space_sz-sz)
                break

    ans = 0
    for i, c in enumerate(FINAL):
        if c is not None:
            ans += i*c
    return ans


p1 = solve(False)
p2 = solve(True)
pr(p1)
pr(p2)
