# pylint: disable=C0114,C0116,C0301,C0209,W1514,C0414,C0200,E0001

from time import perf_counter_ns
from typing import Any
import os

input_file = os.path.join(os.path.dirname(__file__), "input.txt")
# input_file = os.path.join(os.path.dirname(__file__), "test.txt")


def profiler(method):

    def wrapper_method(*args: Any, **kwargs: Any) -> Any:
        start_time = perf_counter_ns()
        ret = method(*args, **kwargs)
        stop_time = perf_counter_ns() - start_time
        time_len = min(9, ((len(str(stop_time))-1)//3)*3)
        time_conversion = {9: 'seconds', 6: 'milliseconds',
                           3: 'microseconds', 0: 'nanoseconds'}
        print(f"Method {method.__name__} took : {
              stop_time / (10**time_len)} {time_conversion[time_len]}")
        return ret

    return wrapper_method


def exec(prog, reg):
    pc = 0
    output = []

    while True:
        if pc > len(prog) - 1:
            return output

        op = prog[pc]
        opreand = prog[pc+1]
        assert 0 <= opreand < 7
        combo = opreand if opreand < 4 else reg[opreand-4]

        if op == 0:  # adv
            reg[0] = reg[0] // 2 ** combo
        elif op == 1:  # bxl
            reg[1] ^= opreand
        elif op == 2:  # bst
            reg[1] = combo % 8
        elif op == 3:  # jnz
            if reg[0] != 0:
                pc = opreand
                continue
        elif op == 4:  # bxl
            reg[1] ^= reg[2]
        elif op == 5:
            output.append(str(combo % 8))
        elif op == 6:  # bdv
            reg[1] = reg[0] // 2 ** combo
        elif op == 7:  # cdv
            reg[2] = reg[0] // 2 ** combo

        pc += 2


@profiler
def part_1():
    with open(input_file) as f:
        ps = f.read().split("\n\n")

    reg = []
    for l in ps[0].splitlines():
        p = l.split(":")
        reg.append(int(p[1]))

    prog = list(map(int, ps[1].split(":")[1].split(",")))
    print(",".join(exec(prog, reg)))

@profiler
def part_2():
    with open(input_file) as f:
        ps = f.read().split("\n\n")

    prog = list(map(int, ps[1].split(":")[1].split(",")))
    to_visit = [(len(prog), 0)]
    while to_visit:
        pos, a = to_visit.pop(0)
        for i in range(8):
            n_a = a*8 + i
            o = list(map(int, exec(prog, [n_a, 0, 0])))
            if o == prog[pos-1:]:
                to_visit.append((pos - 1, n_a))
                if len(o) == len(prog):
                    print(n_a)

if __name__ == "__main__":
    part_1()
    part_2()
