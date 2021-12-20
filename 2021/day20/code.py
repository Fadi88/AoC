from os import XATTR_REPLACE
import time


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

def sim_cycles(cycles):
    
    assert(cycles%2 == 0)
    
    p = open("day20/input.txt").read().split("\n\n")

    algo = p[0].replace("\n", "")
    i = p[1].split("\n")

    lit_pix = set()
    for y, l in enumerate(i):
        for x, c in enumerate(l):
            if c == "#":
                lit_pix.add((x, y))

    for iter in range(cycles):
        new_pix = set()

        xs = [p[0] for p in lit_pix]
        x_l , x_u = min(xs) , max(xs)

        ys = [p[1] for p in lit_pix]
        y_l , y_u = min(ys) , max(ys)

        for x in range(x_l - 1, x_u + 2):
            for y in range(y_l - 1, y_u + 2):
                idx = ""
                for t in range(9):
                    nx = x + t % 3 - 1
                    ny = y + t // 3 - 1
                    if x_l <= nx <= x_u and  y_l <= ny <= y_u :
                        idx += '1' if (nx,ny) in lit_pix else '0'
                    else :
                        idx += '1' if iter%2 == 1 else '0'

                if algo[int(idx, 2)] == "#":
                    new_pix.add((x, y))
        lit_pix = new_pix

    return len(lit_pix)

@profiler
def part1():
    print(sim_cycles(2))


@profiler
def part2():
    print(sim_cycles(50))

if __name__ == "__main__":

    part1()
    part2()
