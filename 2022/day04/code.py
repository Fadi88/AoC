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
    total = 0
    for l in open("input.txt"):
        d1, d2, d3, d4 = list(map(int, l.replace('-', ',').split(',')))
        if (d1 <= d3 and d2 >= d4) or (d3 <= d1 and d4 >= d2):
            total += 1

    print(total)

@profiler
def part2():
    total = 0
    for l in open("input.txt"):
        d1, d2, d3, d4 = list(map(int, l.replace('-', ',').split(',')))
        if d1 <= d3 <= d2 or d1 <= d4 <= d2 or d3 <= d1 <= d4 or d3 <= d2 <= d4:
            total += 1

    print(total)

if __name__ == "__main__":

    part1()
    part2()
