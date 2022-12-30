import time
import re


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print("Method " + method.__name__ + " took : " +
              "{:2.5f}".format(time.time() - t) + " sec")
        return ret

    return wrapper_method


def flip(t):
    return t[::-1]

# https://stackoverflow.com/a/34347121
def rotate(t):
    return [*map("".join, zip(*reversed(t)))]


def get_pattern(rules, sub_grid):
    for _ in range(2):
        sub_grid = flip(sub_grid)
        for _ in range(4):
            sub_grid = rotate(sub_grid)
            if "".join(sub_grid) in rules:
                return rules["".join(sub_grid)]


@profiler
def part1():

    rules = {}
    for l in open("day21/input.txt").read().splitlines():
        p = l.split(" => ")
        rules[p[0].replace("/", "")] = p[1].replace("/", "")

    grid = [".#.", "..#", "###"]

    for _ in range(5):
        new_grid = []

        step = 2 if len(grid) % 2 == 0 else 3

        for dy in range(len(grid) // step):
            pattern_step = 3 if step == 2 else 4
            for _ in range(pattern_step):
                new_grid.append("")
            for dx in range(len(grid) // step):
                sub_grid = [l[dx*step:(dx+1)*step]
                            for l in grid[dy*step:(dy+1)*step]]
                pt = get_pattern(rules,sub_grid)

                for dp in range(len(pt)//pattern_step):
                    new_grid[dy*pattern_step + dp] += pt[pattern_step*dp:pattern_step*(dp+1)]
                
        grid = new_grid

    print(sum(l.count("#") for l in grid))

@profiler
def part2():

    rules = {}
    for l in open("day21/input.txt").read().splitlines():
        p = l.split(" => ")
        rules[p[0].replace("/", "")] = p[1].replace("/", "")

    grid = [".#.", "..#", "###"]

    for _ in range(18):
        new_grid = []

        step = 2 if len(grid) % 2 == 0 else 3

        for dy in range(len(grid) // step):
            pattern_step = 3 if step == 2 else 4
            for _ in range(pattern_step):
                new_grid.append("")
            for dx in range(len(grid) // step):
                sub_grid = [l[dx*step:(dx+1)*step]
                            for l in grid[dy*step:(dy+1)*step]]
                pt = get_pattern(rules,sub_grid)

                for dp in range(len(pt)//pattern_step):
                    new_grid[dy*pattern_step + dp] += pt[pattern_step*dp:pattern_step*(dp+1)]
                
        grid = new_grid

    print(sum(l.count("#") for l in grid))


if __name__ == "__main__":

    part1()
    part2()
