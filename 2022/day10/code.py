from time import perf_counter


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print('Method ' + method.__name__ + ' took : ' +
              "{:2.5f}".format(perf_counter()-t) + ' sec')
        return ret
    return wrapper_method


@profiler
def part1():
    x = 1
    cycle = 0
    strength = {}


    for l in open("input.txt").read().splitlines():
        if "addx" in l:
            cycle += 1
            strength[cycle] = (x, x * cycle)
            cycle += 1
            strength[cycle] = (x, x * cycle)
            x += int(l.split(" ")[1])
        else:
            cycle += 1
            strength[cycle] = (x, x * cycle)

    print(sum([strength[cycle][1] for cycle in [20,60,100,140,180,220]]))


@profiler
def part2():
    x = 1
    cycle = 0
    strength = {}

    for l in open("input.txt").read().splitlines():
        if "addx" in l:
            cycle += 1
            strength[cycle] = (x, x * cycle)
            cycle += 1
            strength[cycle] = (x, x * cycle)
            x += int(l.split(" ")[1])
        else:
            cycle += 1
            strength[cycle] = (x, x * cycle)

    screen = [[' ' for x in range(40)] for y in range(6)]

    for cycle in strength:
        x = strength[cycle][0]
        if (cycle-1)%40 in [x-1,x,x+1]:
            screen[(cycle-1)//40][(cycle-1)%40] = "0"

    for l in screen:
        print("".join(l))


if __name__ == "__main__":

    part1()
    part2()
