import time,os

def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        method(*arg, **kw)
        print('Method '  + method.__name__ +' took : ' + "{:2.5f}".format(time.time()-t) + ' sec')
    return wrapper_method

def is_triangle(a,b,c):
    return a + b > c and a + c > b and b + c > a

@profiler
def part1():

    with open('input.txt') as f_in :
        ls = [list(map(int,l.split())) for l in f_in.read().strip().split('\n')]

    cnt = 0
    for l in ls:
        if is_triangle(l[0],l[1],l[2]):
            cnt += 1

    print(cnt)


@profiler
def part2():

    with open('input.txt') as f_in :
        ls = [list(map(int,l.split())) for l in f_in.read().strip().split('\n')]

    cnt = 0
    for c in range(3):
        new_l = [t[c] for t in ls]

        for i in range(0,len(new_l),3):
            if is_triangle(new_l[i] , new_l[i+1] , new_l[i+2]) :
                cnt += 1

    print(cnt)





if __name__ == "__main__":

    part1()
    part2()
