import time,os,re

def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        method(*arg, **kw)
        print('Method '  + method.__name__ +' took : ' + "{:2.5f}".format(time.time()-t) + ' sec')
    return wrapper_method

@profiler
def part1():

    cnt = 0
    l_idx = 0
    dx , dy = (3,1)
    with open('input.txt', 'r') as f_in:
        for l in f_in:
            if l_idx % len(l.strip())== 0:
                y = 0
            else:
                y = (dx * l_idx) % len(l.strip())
            if l[y] == '#':
                cnt += 1

            l_idx += dy
        print("part 1 : " ,cnt)



@profiler
def part2():
        
    
    trials = [(1,1) , (3,1) , (5,1) , (7,1) , (1,2)]
    prod = 1
    for dx, dy in trials:
        with open('input.txt', 'r') as f_in:
            cnt = 0
            l_idx = 0
            for l in f_in:
                if l_idx % dy != 0:
                    l_idx += 1
                    continue

                if l_idx % len(l.strip())== 0:
                    y = 0
                else:
                    y = (dx * l_idx) % len(l.strip())
                if l[y] == '#':
                    cnt += 1
                l_idx += 1

            print(cnt)
            prod *= cnt
    print("part 2 : " ,prod)

if __name__ == "__main__":

    part1()
    part2()