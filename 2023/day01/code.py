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

    for l in open("day01/input.txt"):
        d = re.findall(r"\d" , l)

        total += int(d[0] + d[-1])

    print(total)

@profiler
def part2():

    vals = {
        "one" : "1",
        "two" : "2",
        "three" : "3",
        "four" : "4",
        "five" : "5",
        "six" : "6",
        "seven" : "7",
        "eight" : "8",
        "nine" : "9",
        "zero" : "0",

    }
    total = 0

    for l in open("day01/input.txt"):
        words = re.findall("(?=(" + "|".join(vals.keys()) + "|\d))" , l)
     
        total += int("".join([ d if d.isdigit() else vals[d] for d in [words[0] , words[-1]]]))
        
    print(total)

if __name__ == "__main__":

    part1()
    part2()
