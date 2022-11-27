import time
from collections import defaultdict


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


def sim(p, t):
    return (p[0] + p[2] * t, p[1] + p[3] * t)


@profiler
def part_1():
    p = open("day12/input.txt").read().split("\n\n")

    offset = 0
    state =  p[0].split(":")[1].strip()

    mapping = {}
    for t in p[1].split("\n"):
        ps = t.split(" => ")
        mapping[ps[0]] = ps[1]

    for _ in range(20):
        n_state = ""
        for i in range(2,len(state) - 5):
            n_state += mapping[state[i-2 : i + 3]]
        state = "....." + n_state + "....."
        offset += 5

    s = sum([i - offset for i in range(len(state)) if state[i] == "#"])
    print(s)


@profiler
def part_2():
    p = open("day12/input.txt").read().split("\n\n")

    offset = 10
    state = p[0].split(":")[1].strip()

    mapping = defaultdict(lambda: ".")
    for t in p[1].split("\n"):
        ps = t.split(" => ")
        mapping[ps[0]] = ps[1]

    offset = 0
    cnt = 0
    while True:
        cnt += 1
        state = "....." + state + "....."
        offset += 5
        n_state = ""
        for i in range(2, len(state) - 2):
            n_state += mapping[state[i - 4 : i + 1]]

        # at this point the pattern just repeates while adding an offset each cycle
        if state.strip(".") == n_state.strip("."):
            break
        state = n_state.rstrip(".")

    # how many places does the pattern move when its repeating
    repetation_offset = state.find("#") - n_state.find("#")

    s = sum(
        [
            i - offset - (50000000000 - cnt) * repetation_offset
            for i in range(len(n_state))
            if n_state[i] == "#"
        ]
    )
    print(s)


if __name__ == "__main__":

    part_1()
    part_2()
