# pylint: disable=C0114,C0116,C0301,C0209,W1514,C0414

from collections import defaultdict, Counter, deque
import sys
from time import time as perf_counter
from typing import Any
import os
import re

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
        disk = f.read().strip()

    # disk = "23331331214141314020000"

    layout = []

    for id in range(len(disk)):
        ch = id // 2 if id % 2 == 0 else "."
        layout.extend([ch] * int(disk[id]))

    while layout.count("."):
        pos = layout.index(".")
        n = layout.pop()
        layout[pos] = n

        while layout[-1] == ".":
            layout.pop()

    print(sum(c*i for i, c in enumerate(layout)))


def clean_free(free_space):

    new_free_space = []
    free_space.sort(key=lambda x: x[0])

    for fpos, fsize in free_space:
        if fsize == 0:
            continue
        if len(new_free_space) == 0:
            new_free_space.append((fpos, fsize))
        else:
            if new_free_space[-1][0] + new_free_space[-1][1] == fpos:
                new_free_space[-1] = (new_free_space[-1]
                                      [0], new_free_space[-1][1] + fsize)
            else:
                new_free_space.append((fpos, fsize))

    return new_free_space


@profiler
def part_2():
    with open(input_file) as f:
        disk = f.read().strip()

    # disk = "23331331214141314020000"
    pos = 0

    files = []  # (id,pos,size)
    free_space = []  # (pos,size)

    pos = 0
    for id in range(len(disk)):

        size = int(disk[id])

        if id % 2 == 0:
            files.append((id//2, pos, size))
        else:
            free_space.append((pos, size))

        pos += size

    for fidx in range(len(files))[::-1]:
        fid, fpos, fsize = files[fidx]
        if fsize == 0:
            continue

        for i in range(len(free_space)):
            free_pos, free_size = free_space[i]

            if fsize <= free_size and free_pos < fpos:
                files[fidx] = (fid, free_pos, fsize)

                if free_size == fsize:
                    free_space.pop(i)
                else:
                    free_space[i] = (free_pos + fsize, free_size - fsize)

                free_space.append((fpos, fsize))

                free_space = clean_free(free_space)

                break

    print(sum((fpos + i) * fid for fid, fpos,
          fsize in files for i in range(fsize)))


if __name__ == "__main__":
    part_1()
    part_2()
