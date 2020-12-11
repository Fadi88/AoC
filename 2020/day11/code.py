import time,os

def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print('Method '  + method.__name__ +' took : ' + "{:2.5f}".format(time.time()-t) + ' sec')
        return ret
    return wrapper_method

def sim_cycle_p1(ls):

    switched = False
    ret = ls.copy()
    steps = [(0,1) , (0,-1) , (1,0) , (-1 , 0) , (1 , 1) , (-1 , -1) , (-1 , 1), (1 , -1)]
    for i in range(len(ls)):
        for t in range(len(ls[i])):
            if ls[i][t] == 'L':
                cnt = 0
                for dx,dy in steps:
                    x = i + dx
                    y = t + dy
                    if x < 0 or x == len(ls) or y < 0 or y == len(ls[i]):
                        continue
                    if ls[x][y] == '#':
                        cnt += 1

                if cnt == 0:
                    ret[i] = ret[i] = ret[i][:t] + '#' + ret[i][t + 1 :]
                    switched = True

            elif ls[i][t] == '#':
                cnt = 0
                for dx,dy in steps:
                    x = i + dx
                    y = t + dy
                    if x < 0 or x == len(ls) or y < 0 or y == len(ls[i]):
                        continue
                    if ls[x][y] == '#':
                        cnt += 1

                    if cnt >= 4:
                        ret[i] = ret[i][:t] + 'L' + ret[i][t + 1 :]
                        switched = True


    return ret,switched

def sim_cycle_p2(ls):

    switched = False
    ret = ls.copy()
    directions = [(0,1) , (0,-1) , (1,0) , (-1 , 0) , (1 , 1) , (-1 , -1) , (-1 , 1), (1 , -1)]
    for i in range(len(ls)):
        for t in range(len(ls[i])):
            if ls[i][t] == 'L':
                cnt = 0
                for dx,dy in directions:
                    for fac in range(1,31) :
                        x = i + fac * dx
                        y = t + fac *dy
                        if x < 0 or x == len(ls) or y < 0 or y == len(ls[i]):
                            break
                        if ls[x][y] == '#':
                            cnt += 1
                        if ls[x][y] == '#' or ls[x][y] == 'L':
                            break


                if cnt == 0:
                    ret[i] = ret[i] = ret[i][:t] + '#' + ret[i][t + 1 :]
                    switched = True

            elif ls[i][t] == '#':
                cnt = 0

                for dx,dy in directions:
                    for fac in range(1,31) :
                        x = i + fac * dx
                        y = t + fac * dy
                        if x < 0 or x == len(ls) or y < 0 or y == len(ls[i]):
                            break
                        if ls[x][y] == '#':
                            cnt += 1
                        if ls[x][y] == '#' or ls[x][y] == 'L':
                            break

                    if cnt >= 5:
                        ret[i] = ret[i][:t] + 'L' + ret[i][t + 1 :]
                        switched = True


    return ret,switched

@profiler
def part1():

    ls = open('input.txt', 'r').read().split('\n')
    cnt = 0
    while True :
        cnt += 1
        ls,switch = sim_cycle_p1(ls)
        if not switch:
            break
    
    chairs = 0
    for l in ls:
        for c in l:
            if c == '#':
                chairs += 1

    print('part 1 answer : ' , chairs)

    

@profiler
def part2():

    ls = open('input.txt', 'r').read().split('\n')
    cnt = 0
    while True :
        cnt += 1
        ls,switch = sim_cycle_p2(ls)
        if not switch:
            break
    
    chairs = 0
    for l in ls:
        for c in l:
            if c == '#':
                chairs += 1

    print('part 2 answer : ' , chairs)

if __name__ == "__main__":
    

    part1()
    part2()

    
    