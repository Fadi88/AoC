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
    l = open("input.txt").read()
    target_len = 4
    for i in range(target_len-1, len(l)):
        if len(set(l[i-target_len:i])) == target_len:
            print(i)
            break


@profiler
def part2():
    l = open("input.txt").read()
    target_len = 14
    for i in range(target_len-1, len(l)):
        if len(set(l[i-target_len:i])) == target_len:
            print(i)
            break

if __name__ == "__main__":

    part1()
    part2()
