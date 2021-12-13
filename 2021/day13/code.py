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


def fold_grid(dots, fold):

    axe, loc = fold
    if axe == "x":
        return {(loc - (p[0] - loc), p[1]) if p[0] > loc else p for p in dots}
    else:
        return {(p[0], loc - (p[1] - loc)) if p[1] > loc else p for p in dots}


@profiler
def part1():
    dots = set()
    fold = []
    for l in open("day13/input.txt"):
        if "," in l:
            dots.add(tuple(map(int, l.strip().split(","))))
        elif "fold" in l:
            p = l.split("=")
            fold.append(tuple((p[0][-1], int(p[1]))))

    dots = fold_grid(dots, fold[0])

    print(len(dots))


@profiler
def part2():
    dots = set()
    fold = []
    for l in open("day13/input.txt"):
        if "," in l:
            dots.add(tuple(map(int, l.strip().split(","))))
        elif "fold" in l:
            p = l.split("=")
            fold.append(tuple((p[0][-1], int(p[1]))))

    for f in fold:
        dots = fold_grid(dots, f)

    max_x = max([p[0] for p in dots])
    max_y = max([p[1] for p in dots])

    for y in range(max_y + 1):
        for x in range(max_x + 1):
            if (x, y) in dots:
                print("#", end="")
            else:
                print(" ", end="")
        print()


if __name__ == "__main__":

    part1()
    part2()
