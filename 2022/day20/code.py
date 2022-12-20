from time import time as perf_counter


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
    input = [int(l) for l in open("input.txt")]

    buffer = [(idx, i) for idx, i in enumerate(input)]

    for idx, i in enumerate(input):
        old_idx = buffer.index((idx, i))

        buffer.remove((idx, i))
        buffer.insert((old_idx + i + len(input) - 1) %
                      (len(input) - 1), (-1, i))

    zero_idx = buffer.index((-1, 0))

    print(sum(buffer[(zero_idx + (i+1) * 1000) % len(buffer)][1]
          for i in range(3)))


@profiler
def part2():
    input = [int(l) * 811589153 for l in open("input.txt")]

    buffer = [(idx, i) for idx, i in enumerate(input)]

    for _ in range(10):
        for idx, i in enumerate(input):
            old_idx = buffer.index((idx, i))

            buffer.remove((idx, i))
            buffer.insert((old_idx + i + len(input) - 1) %
                          (len(input) - 1), (idx, i))

    zero_idx = buffer.index((input.index(0), 0))
    print(sum(buffer[(zero_idx + (i+1) * 1000) % len(buffer)][1]
          for i in range(3)))


if __name__ == "__main__":

    part1()
    part2()
