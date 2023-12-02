from time import perf_counter
import re

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
    total = 0

    for l in open("day02/input.txt"):

        red_cnt =  max(map(int,re.findall(r"(\d+) red",l)))
        green_cnt =  max(map(int,re.findall(r"(\d+) green",l)))
        blue_cnt =  max(map(int,re.findall(r"(\d+) blue",l)))

        id =  int(re.findall(r"Game (\d+)",l)[0])

        if red_cnt <= 12 and green_cnt <=13 and blue_cnt<=14:
            total += id

    print(total)


@profiler
def part2():
    total = 0

    for l in open("day02/input.txt"):

        red_cnt =  max(map(int,re.findall(r"(\d+) red",l)))
        green_cnt =  max(map(int,re.findall(r"(\d+) green",l)))
        blue_cnt =  max(map(int,re.findall(r"(\d+) blue",l)))

        total += red_cnt * green_cnt * blue_cnt

    print(total)


if __name__ == "__main__":

    part1()
    part2()
