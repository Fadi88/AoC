from time import perf_counter
from copy import deepcopy


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
    grid = []
    for l in open("input.txt").read().splitlines():
        grid.append(list(map(int, l)))

    vis = set()

    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if x in [0, len(grid[0])-1] or y in [0, len(grid)-1]:
                vis.add((x, y))

            else:
                right = grid[y][0:x]
                left = grid[y][x+1:]
                top = [r[x] for r in grid[0:y]]
                button = [r[x] for r in grid[y+1:]]

                if all(map(lambda v: v < grid[y][x], right)) or all(map(lambda v: v < grid[y][x], left)) or all(map(lambda v: v < grid[y][x], top)) or all(map(lambda v: v < grid[y][x], button)):
                    vis.add((x, y))

    print(len(vis))


def get_score(val, direction):
    score = 0
    for tree in direction:
        if val > tree:
            score += 1
        else:
            return score + 1
    return score


@profiler
def part2():
    grid = []
    for l in open("input.txt").read().splitlines():
        grid.append(list(map(int, l)))

    score = deepcopy(grid)

    for y in range(len(grid)):
        for x in range(len(grid[0])):

            left = grid[y][0:x][::-1]
            right = grid[y][x+1:]
            top = [r[x] for r in grid[0:y]][::-1]
            bottom = [r[x] for r in grid[y+1:]]

            score[y][x] = get_score(grid[y][x], right) * get_score(
                grid[y][x], left) * get_score(grid[y][x], top) * get_score(grid[y][x], bottom)

    print(max(map(max, score)))


if __name__ == "__main__":

    part1()
    part2()
