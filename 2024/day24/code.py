# pylint: disable=C0114,C0116,C0301,C0209,W1514,C0414,E0001,R0914

from typing import Any
import os
from time import perf_counter_ns
import re

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


def get_value(reg, wires, xs, ys):
    if re.match(r"x\d+", reg):
        return xs[reg]
    if re.match(r"y\d+", reg):
        return ys[reg]
    if reg in wires:
        return wires[reg]

    return None


def get_num(d, c):
    top = max(int(i[1:]) for i in d if re.match(c + r"\d+", i))
    ret = ""
    for i in range(top, -1, -1):
        try:
            ret += str(d[c + f"{i:02d}"])
        except KeyError:
            return -1
    return int(ret, 2)


def eval_loop(res, xs, ys):
    wires = {}
    while len(wires) < len(res):
        for d in res:
            op = res[d]

            v1 = get_value(op[0], wires, xs, ys)
            v2 = get_value(op[2], wires, xs, ys)

            if v1 is not None and v2 is not None:
                if op[1] == "AND":
                    wires[d] = v1 & v2
                elif op[1] == "OR":
                    wires[d] = v1 | v2
                elif op[1] == "XOR":
                    wires[d] = v1 ^ v2
    return get_num(wires, "z")


def get_new_res(mapping, res):
    rev_mapping = {v: k for k, v in mapping.items()}
    new_res = {}
    for d in res:
        if re.match(r"z\d+", d):
            num = int(d[1:])
            if num in mapping:
                pass
            elif num in rev_mapping:
                pass
        new_res[d] = res[d]

    return new_res


@profiler
def part_1():
    with open(input_file) as f:
        data = f.read().split("\n\n")

    xs, ys = {}, {}
    for l in data[0].splitlines():
        d = xs if "x" in l else ys
        ps = l.split(":")
        d[ps[0]] = int(ps[1])

    res = {}
    for l in data[1].splitlines():
        ps = l.split()
        assert ps[4] not in res
        res[ps[4]] = (ps[0], ps[1], ps[2])

    print(eval_loop(res, xs, ys))


@ profiler
def part_2():
    with open(input_file) as f:
        data = f.read().split("\n\n")

    xs, ys = {}, {}

    for l in data[0].splitlines():
        d = xs if "x" in l else ys
        ps = l.split(":")
        d[ps[0]] = int(ps[1])

    ops = {}
    rev_ops = {}

    for l in data[1].splitlines():
        ps = l.split()
        assert ps[4] not in ops
        ops[ps[4]] = (ps[0], ps[1], ps[2])

        rev_ops[(ps[0], ps[1], ps[2])] = ps[4]
        rev_ops[(ps[2], ps[1], ps[0])] = ps[4]

    top = max({int(d[1:]) for d in ops if re.match(r"z\d+", d)})

    wrong_gates = set()

    for i in range(1, top):
        x = f"x{i:02d}"
        y = f"y{i:02d}"
        z = f"z{i:02d}"

        res_op = ops[z]

        xor_gate = rev_ops[(x, "XOR", y)]
        and_gate = rev_ops[(x, "AND", y)]

        if "XOR" not in res_op:
            wrong_gates.add(z)

        carry = [set(o).difference({"XOR", xor_gate})
                 for o in ops.values() if "XOR" in o and xor_gate in o]
        if len(carry) != 1:
            wrong_gates.add(xor_gate)
            wrong_gates.add(and_gate)
        else:
            carry = carry[0].pop()
            xor2_gate = rev_ops[(xor_gate, "XOR", carry)]
            if xor2_gate != z:
                wrong_gates.add(xor2_gate)

    print(",".join(sorted(list(wrong_gates))))


if __name__ == "__main__":
    part_1()
    part_2()
