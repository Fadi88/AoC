# pylint: disable=C0114,C0116,C0301,C0209,W1514

from time import perf_counter

def profiler(method):
    def wrapper_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print(
            "Method "
            + method.__name__
            + " took : "
            + "{:2.5f}".format(perf_counter() - t)
            + " sec"
        )
        return ret

    return wrapper_method

def is_safe(l):
    if l not in [sorted(l), sorted(l)[::-1]]:
        return False
    for i in range(1,len(l)):
        if abs(l[i] - l[i-1]) not in [1,2,3]:
            return False
    return True

@profiler
def part1():
    reports = [ list(map(int,l.split())) for l in open("day02/input.txt").readlines()]
    print(sum(is_safe(l) for l in reports))

def is_safe_tolerate(i):
    return any(is_safe(i[:j]+i[j+1:]) for j in range(len(i)))
  
@profiler
def part2():
    reports = [ list(map(int,l.split())) for l in open("day02/input.txt").readlines()]
    print(sum(is_safe_tolerate(l) for l in reports))


if __name__ == "__main__":
    part1()
    part2()
