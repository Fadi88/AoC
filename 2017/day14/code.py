from os import altsep
import time
from functools import reduce


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print(
            "Method "
            + method.__name__
            + " took : "
            + "{:2.5f}".format(time.time() - t)
            + " sec"
        )
        return ret
    return wrapper_method


def reverse_section(circle, pos, l):
    for i in range(l // 2):
        tmp = circle[(pos + i) % len(circle)]
        circle[(pos + i) % len(circle)] = circle[(pos + l - i - 1) % len(circle)]
        circle[(pos + l - i - 1) % len(circle)] = tmp


def get_hash(st):

    inp = list(map(ord, st))
    inp += [17, 31, 73, 47, 23]
    circle = list(range(256))

    skip = 0
    pos = 0
    for _ in range(64):
        for n in inp:
            reverse_section(circle, pos, n)

            pos = (pos + n + skip) % len(circle)

            skip += 1

    dense_hash = [
        reduce(lambda a, b: a ^ b, circle[i * 16 + 0 : i * 16 + 16]) for i in range(16)
    ]

    return "".join(map(lambda d: hex(d)[2:].zfill(2), dense_hash))

input = "nbysizxe"
#input = "flqrgnkx"

@profiler
def part1():

    sum = 0
    ret = []
    for i in range(128):
        ret.append(bin(int(get_hash(input + "-" + str(i)),16))[2:].zfill(128))
        sum += ret[-1].count('1')

    print(sum)

    return ret

@profiler
def part2(grid):


    visited = set()

    deltas = [(0,1) , (0,-1) , (1,0) , (-1,0)]

    clusters = 0
    
    reg = []

    for y,l in enumerate(grid):
        for x,c in enumerate(l):
            if c == "1" and (x,y) not in visited:
                to_visit = [(x,y)]

                while len(to_visit) > 0:
                    c_x,c_y = to_visit.pop()

                    visited.add((c_x,c_y))

                    for dx,dy in deltas:
                        if 0 <= c_x+dx < len(grid[0]) and 0 <= c_y+dy < len(grid):
                            if grid[c_y+dy][c_x+dx] == '1' and (c_x+dx,c_y+dy) not in visited:
                                to_visit.append((c_x+dx,c_y+dy))

                clusters += 1


    print(clusters)


if __name__ == "__main__":

    m = part1()
    part2(m)
