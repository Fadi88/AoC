import time

def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print('Method ' + method.__name__ + ' took : ' +
              "{:2.5f}".format(time.time()-t) + ' sec')
        return ret
    return wrapper_method


def get_nums(l):
    ps = l.strip().split()
    return (int(ps[3]), int(ps[-1][:-1]))


@profiler
def part_1():
    with open('day15/input.txt') as f:
        inp = [get_nums(l) for l in f.readlines()]

    itter = 0
    while not all((itter + i + disc[1]) % disc[0] == 0 for i, disc in enumerate(inp)):
        itter += 1

    print(itter-1)

@profiler
def part_2():
    with open('day15/input.txt') as f:
        inp = [get_nums(l) for l in f.readlines()]
    inp.append((11, 0))

    itter = 0
    while not all((itter + i + disc[1]) % disc[0] == 0 for i, disc in enumerate(inp)):
        itter += 1

    print(itter-1)

if __name__ == "__main__":

    part_1()
    part_2()
