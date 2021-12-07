import time


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print('Method ' + method.__name__ + ' took : ' +
              "{:2.5f}".format(time.time()-t) + ' sec')
        return ret
    return wrapper_method


@profiler
def part1():
    input = list(map(int, open("day07/input.txt").read().split(',')))

    p1 = min([sum(map(lambda x:  abs(x-i), input)) for i in range(max(input))])

    print("part 1 : ", p1)


def get_fuel(dist):
    return dist * (dist + 1) // 2


@profiler
def part2():
    input = list(map(int, open("day07/input.txt").read().split(',')))

    p2 = min([sum(map(lambda x:  get_fuel(abs(x-i)), input)) for i in range(max(input))])

    print("part 2 : ", p2)


if __name__ == "__main__":

    part1()
    part2()
