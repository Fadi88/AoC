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
    input = [int(i) for i in open("day06/input.txt").read().split(',')]

    for _ in range(80):
        tmp = []
        for i in input:
            if i == 0:
                tmp.append(8)
                tmp.append(6)
            else:
                tmp.append(i-1)

        input = tmp

    print(len(tmp))


@profiler
def part2():

    input = [int(i) for i in open("day06/input.txt").read().split(',')]

    tracker = {i: 0 for i in range(9)}

    for i in input:
        tracker[i] += 1

    for _ in range(256):
        tmp = {i: 0 for i in range(9)}
        for i in tracker:
            if i == 0:
                tmp[8] += tracker[0]
                tmp[6] += tracker[0]
            else:
                tmp[i-1] += tracker[i]

        tracker = tmp

    print(sum(tracker.values()))


if __name__ == "__main__":

    part1()
    part2()
