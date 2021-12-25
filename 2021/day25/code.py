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


@profiler
def part1():
    grid = [list(l.strip())for l in open("day25/input.txt")]

    east = set()
    south = set()

    max_x = len(grid[0])
    max_y = len(grid)

    for y, l in enumerate(grid):
        for x,c in enumerate(l):
            if c == ">":
                east.add((x,y))
            elif c == "v":
                south.add((x,y))

    cnt = 0
    while True:
        new_east = set()
        new_south = set()

        for e in east:
            n_p = ((e[0]+1)%max_x , e[1])
            if n_p not in east and n_p not in south:
                new_east.add(n_p)
            else:
                new_east.add(e)

        for s in south:
            n_p = (s[0] , (s[1]+1)%max_y)
            if n_p not in south and n_p not in new_east:
                new_south.add(n_p)
            else:
                new_south.add(s)

        cnt += 1

        if new_south == south and east == new_east:
            break
        south = new_south
        east = new_east

    print(cnt)



if __name__ == "__main__":

    part1()
