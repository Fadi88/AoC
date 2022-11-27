import time
from collections import defaultdict
from copy import deepcopy


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


@profiler
def part1():

    prog = [l for l in open("day18/input.txt").read().split("\n")]

    reg = defaultdict(int)

    pc = 0

    last_freq = 0

    while pc < len(prog):
        i = prog[pc].split(" ")

        if len(i) == 3:
            if i[2] in reg:
                val = reg[i[2]]
            else:
                try:
                    val = int(i[2])
                except:
                    breakpoint()

        if i[0] == "snd":
            last_freq = reg[i[1]]
        elif i[0] == "set":
            reg[i[1]] = val
        elif i[0] == "add":
            reg[i[1]] += val
        elif i[0] == "mul":
            reg[i[1]] *= val
        elif i[0] == "mod":
            reg[i[1]] %= val
        elif i[0] == "rcv":
            print(last_freq)
            break
        elif i[0] == "jgz":
            if reg[i[1]] != 0:
                pc += val
                if pc == 0 or pc == len(prog) - 1:
                    break
                continue
        pc += 1


class app:
    def __init__(self, id, prog) -> None:
        self.pc = 0
        self.reg = defaultdict(int)
        self.reg["p"] = id
        self.prog = deepcopy(prog)
        self.input = []
        self.output = []
        self.termineated = False
        self.waitting_input = False

    def get_output(self):
        tmp = deepcopy(self.output)
        self.output = []
        return tmp

    def set_input(self, input):
        if type(input) == int:
            self.input.append(input)
        else:
            self.input += input

        self.waitting_input = False

    def cycle(self):
        if self.termineated:
            assert False

        while self.pc < len(self.prog):
            i = self.prog[self.pc].split(" ")

            if len(i) == 3:
                if i[2] in self.reg:
                    val = self.reg[i[2]]
                else:
                    try:
                        val = int(i[2])
                    except:
                        breakpoint()

            if i[0] == "snd":
                self.output.append(self.reg[i[1]])
            elif i[0] == "set":
                self.reg[i[1]] = val
            elif i[0] == "add":
                self.reg[i[1]] += val
            elif i[0] == "mul":
                self.reg[i[1]] *= val
            elif i[0] == "mod":
                self.reg[i[1]] %= val
            elif i[0] == "rcv":
                if len(self.input) == 0:
                    self.waitting_input = True
                    return
                self.reg[i[1]] = self.input.pop()
            elif i[0] == "jgz":
                if self.reg[i[1]] > 0:
                    self.pc += val
                    if self.pc == 0 or self.pc == len(self.prog) - 1:
                        self.termineated = True
                    continue
            self.pc += 1


@profiler
def part2():
    prog = [l for l in open("day18/input.txt").read().split("\n")]

    app0 = app(0, prog)
    app1 = app(1, prog)

    cnt = 0
    while True:
        app0.cycle()
        app0_out = app0.get_output()

        app1.set_input(app0_out)
        app1.cycle()
        app1_out = app1.get_output()

        app0.set_input(app1_out)

        cnt += len(app1_out)

        print(cnt)
        if app0.waitting_input and app1.waitting_input and len(app0_out) == 0 and len(app1_out) == 0:
            break

        if app0.termineated and app1.termineated:
            break

    print(cnt)

if __name__ == "__main__":

    part1()
    part2()

