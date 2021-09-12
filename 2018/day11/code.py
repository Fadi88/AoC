import time


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print('Method ' + method.__name__ + ' took : ' +
              "{:2.5f}".format(time.time()-t) + ' sec')
        return ret
    return wrapper_method

puzzle_input = 8199

def get_cell_power(x,y):
    rack_id = x + 10
    power_level = rack_id * y
    power_level += puzzle_input
    power_level *= rack_id

    return (power_level/100)%10 -5 

@profiler
def part_1():
    highest = 0
    pt = (0,0)
    for x in range(2,300):
        for y in range(2,300):
            power = 0
            for dx in range(3):
                for dy in range(3):
                    power += get_cell_power(x+dx,y+dy)

            if power > highest :
                highest = power
                pt = (x,y)

    print(pt,highest)


@ profiler
def part_2():
    grid = [[0] * 300] * 300


    for x in range(300):
        for y in range(300):
            grid[x][y] = get_cell_power(x+1,y+1)


    for sz in range(1,300):
        pass

    

if __name__ == "__main__":

    part_1()
    part_2()
