import time
import re


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print("Method " + method.__name__ + " took : " +
              "{:2.5f}".format(time.time() - t) + " sec")
        return ret

    return wrapper_method


@profiler
def part1():

    input = open("day25/input.txt").read().split("\n\n")

    cycles = int(re.findall(r"\d+", input[0])[0])

    states = {}
    for s in input[1:]:
        s = s.splitlines()

        name = s[0][-2]
        w_false = int(s[2][-2])
        d_false = 1 if "right" in s[3] else -1
        s_false = s[4][-2]

        w_true = int(s[6][-2])
        d_true = 1 if "right" in s[7] else -1
        s_true = s[8][-2]

        states[name] = (w_false, d_false, s_false, w_true, d_true, s_true)

    ones = set()
    pos = 0
    current_state = "A"

    for _ in range(cycles):
        if pos not in ones:
            if states[current_state][0] == 1:
                ones.add(pos)
            pos += states[current_state][1]
            current_state = states[current_state][2]
        else:
            if states[current_state][3] == 0:
                ones.remove(pos)
            pos += states[current_state][4]
            current_state = states[current_state][5]

    print(len(ones))


if __name__ == "__main__":

    part1()
