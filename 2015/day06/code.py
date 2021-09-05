import time,os,re

def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        method(*arg, **kw)
        print('Method '  + method.__name__ +' took : ' + "{:2.5f}".format(time.time()-t) + ' sec')
    return wrapper_method


@profiler
def part1():
    grid = [ [False for _ in range(1000)] for _ in range(1000)]
    with open('input.txt', 'r') as f:
        for l in f:
            l = l.strip()
            d = [*map(int , list(re.findall(r'\d+' , l)))]
            for x in range(d[0] , d[2] + 1):
                for y in range(d[1] , d[3] + 1):
                    if 'toggle' in l:
                        grid[x][y] = not grid[x][y]
                    elif 'on' in l:
                        grid[x][y] = True
                    elif 'off' in l:
                         grid[x][y] = False

        print(sum([sum(l) for l in grid]))
            

@profiler
def part2():
    grid = [ [0 for _ in range(1000)] for _ in range(1000)]
    with open('input.txt', 'r') as f:
        for l in f:
            l = l.strip()
            d = [*map(int , list(re.findall(r'\d+' , l)))]
            for x in range(d[0] , d[2] + 1):
                for y in range(d[1] , d[3] + 1):
                    if 'toggle' in l:
                        grid[x][y] += 2
                    elif 'on' in l:
                        grid[x][y] += 1
                    elif 'off' in l:
                        grid[x][y] = max(grid[x][y] - 1 ,0)

        print(sum([sum(l) for l in grid]))


if __name__ == "__main__":

    part1()
    part2()
