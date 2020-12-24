import time,os,re
from collections import defaultdict
from copy import deepcopy

def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print('Method '  + method.__name__ +' took : ' + "{:2.5f}".format(time.time()-t) + ' sec')
        return ret
    return wrapper_method

@profiler
def part1(inp):

    grid = defaultdict(bool)

    # https://www.redblobgames.com/grids/hexagons/#:~:text=The%20vertical%20distance%20between%20adjacent,match%20an%20exactly%20regular%20polygon.

    dr = {'e' : (1,0) , 'w' : (-1,0) , 'ne' : (0,1) , 'nw' : (-1,1) , 'sw' : (0,-1) , 'se' :(1,-1)}
    for tile in inp:
        x,y = 0,0
        while tile:
            if tile[0] == 'n' or tile[0] == 's':
                t = dr[tile[:2]]
                x += t[0]
                y += t[1]
                tile = tile[2:]
            else :
                t = dr[tile[:1]]
                x += t[0]
                y += t[1]
                tile = tile[1:]

        grid[(x,y)] = not grid[(x,y)]

    print(sum(grid.values()))


@profiler
def part2(inp):

    grid = defaultdict(bool)

    # https://www.redblobgames.com/grids/hexagons/#:~:text=The%20vertical%20distance%20between%20adjacent,match%20an%20exactly%20regular%20polygon.

    dr = {'e' : (1,0) , 'w' : (-1,0) , 'ne' : (0,1) , 'nw' : (-1,1) , 'sw' : (0,-1) , 'se' :(1,-1)}
    for tile in inp:
        x,y = 0,0
        while tile:
            if tile[0] == 'n' or tile[0] == 's':
                t = dr[tile[:2]]
                x += t[0]
                y += t[1]
                tile = tile[2:]
            else :
                t = dr[tile[:1]]
                x += t[0]
                y += t[1]
                tile = tile[1:]

        grid[(x,y)] = not grid[(x,y)]

    living_grid = {t for t in grid if grid[t]}

    for _ in range(100):
        reach = defaultdict(int)
        for b in living_grid:
            for dr_tmp in dr.values():
                reach[(b[0]+dr_tmp[0],b[1]+dr_tmp[1])] += 1

        tmp_grid = set()
        for ele in reach:
            if reach[ele] == 2 and ele not in living_grid:
                tmp_grid.add(ele)
        for ele in living_grid:
            if reach[ele] in [1,2]:
                tmp_grid.add(ele)

        living_grid = tmp_grid

    print(len(living_grid))

if __name__ == "__main__":
    
    inp = open('input.txt').read().split()

    part1(deepcopy(inp))
    part2(deepcopy(inp))
  