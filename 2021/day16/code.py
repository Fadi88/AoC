import operator
import time
from functools import reduce
from operator import mul


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


def parse_versions(p, pos=0):

    if p[pos:].count("1") == 0 or len(p[pos:]) < 7:
        return len(p[pos:]), None

    version = int(p[pos : pos + 3], 2)
    type_id = p[pos + 3 : pos + 6]

    if "".join(type_id) == "100":
        v = 0
        value = []
        while p[pos + 6 + 5 * v] == "1":
            value += p[pos + 7 + 5 * v : pos + 11 + 5 * v]
            v += 1

        value += p[pos + 7 + 5 * v : pos + 11 + 5 * v]
        value = int("".join(value), 2)

        return (6 + 5 * (v + 1), version)

    else:
        if p[pos + 6] == "0":
            packet_len = int("".join(p[pos + 7 : pos + 7 + 15]), 2)
            len_processed = 0
            sub_ver = 0
            while len_processed < packet_len:
                l, v = parse_versions(
                    p[pos + 22 : pos + 22 + packet_len], len_processed
                )
                len_processed += l
                if v is None:
                    break
                sub_ver += v
            return packet_len + 22, version + sub_ver

        else:
            packet_num = int("".join(p[pos + 7 : pos + 7 + 11]), 2)

            sub_ver = 0
            proccessed_len = 0
            for _ in range(packet_num):
                l, v2 = parse_versions(p, pos + 18 + proccessed_len)
                if v2 is None:
                    break
                sub_ver += v2
                proccessed_len += l

            return proccessed_len + 18, version + sub_ver


def perform_op(operation, operand):
    if operation == 0:
        return sum(operand)
    elif operation == -1:
        return reduce(mul, operand, 1)
    elif operation == -2:
        return min(operand)
    elif operation == -3:
        return max(operand)
    elif operation == -5:
        return operand[0] > operand[1]
    elif operation == -6:
        return operand[0] < operand[1]
    elif operation == -7:
        return operand[0] == operand[1]


def parse_values(p, pos=0):

    if p[pos:].count("1") == 0 or len(p[pos:]) < 7:
        return len(p[pos:]), None

    type_id = p[pos + 3 : pos + 6]

    if "".join(type_id) == "100":
        v = 0
        value = []
        while p[pos + 6 + 5 * v] == "1":
            value += p[pos + 7 + 5 * v : pos + 11 + 5 * v]
            v += 1

        value += p[pos + 7 + 5 * v : pos + 11 + 5 * v]
        value = int("".join(value), 2)

        return (6 + 5 * (v + 1), value)

    else:
        operation = int(type_id, 2) * -1
        operands = []

        if p[pos + 6] == "0":
            header = 22
            packet_len = int("".join(p[pos + 7 : pos + 7 + 15]), 2)
            len_processed = 0

            while len_processed < packet_len:
                l, v = parse_values(p[pos + 22 : pos + 22 + packet_len], len_processed)
                len_processed += l
                if v is None:
                    break
                operands.append(v)
            return packet_len + 22, perform_op(operation, operands)

        else:
            header = 18
            packet_num = int("".join(p[pos + 7 : pos + 7 + 11]), 2)

            len_processed = 0
            for _ in range(packet_num):
                l, v = parse_values(p, pos + 18 + len_processed)
                if v is None:
                    break
                operands.append(v)
                len_processed += l

        return len_processed + header, perform_op(operation, operands)


@profiler
def part1():
    pattern = "".join(
        [format(int(c, 16), "04b") for c in open("day16/input.txt").read()]
    )
    _, v = parse_versions(pattern)
    print(v)


@profiler
def part2():
    pattern = "".join(
        [format(int(c, 16), "04b") for c in open("day16/input.txt").read()]
    )

    _, t = parse_values(pattern)

    print(t)


if __name__ == "__main__":

    part1()
    part2()
