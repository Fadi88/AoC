from time import perf_counter
from collections import defaultdict


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
    schematic = open("day03/input.txt").read().splitlines()
 
    checking = False
    valid = False
    num = []
    total = 0

    for y in range(len(schematic)):
        for x in range(len(schematic[0])):

            if schematic[y][x].isdigit():
                num.append(schematic[y][x])
                checking = True
            else:
                if checking and valid:
                    total += int("".join(num))
                checking = False
                valid = False
                num = []
            
            if checking and not valid:
                for dx in [0,-1,1]:
                    for dy in [0,-1,1]:
                        if dx == dy == 0 or  x+dx in [-1,len(schematic[0])] or y+dy in [-1,len(schematic)]:
                            continue
                        
                        if not schematic[y+dy][x+dx].isdigit() and schematic[y+dy][x+dx] != ".":
                            valid = True

    print(total)

@profiler
def part2():
    schematic = open("day03/input.txt").readlines()

    num = []
    gears = defaultdict(set)

    for y in range(len(schematic)):
        for x in range(len(schematic[0])):

            if schematic[y][x].isdigit():
                num.append(schematic[y][x])
            elif len(num) > 0:
                for nx in range(x-len(num)-1,x+1):
                    for ny in range(y-1,y+2):

                        if 0 <= nx < len(schematic[0]) and 0 <= ny < len(schematic) and schematic[ny][nx] == "*":
                            gears[(ny,nx)].add(int("".join(num)))
                num = []

    print(sum([g.pop() * g.pop() for g in gears.values() if len(g) == 2]))


if __name__ == "__main__":

    part1()
    part2()