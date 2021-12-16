import time


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

    if p[pos:].count("1") == 0:
        return 0, None

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

            sub_ver = 0
            proccessed_len = 0
            while proccessed_len < packet_len:
                l, v2 = parse_versions(p, pos + 22 + proccessed_len)
                sub_ver += v2
                proccessed_len += l

            return pos + packet_len, version + sub_ver

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

            return pos + proccessed_len , version + sub_ver


@profiler
def part1():
    pattern = "".join(
        [format(int(c, 16), "04b") for c in open("day16/test.txt").read()]
    )

    print(parse_versions(pattern) , len(pattern))


@profiler
def part2():
    pass


if __name__ == "__main__":

    part1()
    part2()
