import time,re
from collections import defaultdict

def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print('Method '  + method.__name__ +' took : ' + "{:2.5f}".format(time.time()-t) + ' sec')
        return ret
    return wrapper_method

@profiler
def part1():

    ing = []

    with open('input.txt') as f:
        for l in f:
            p = l.strip().split()
            ing.append((int(p[2][:-1]) ,int(p[4][:-1]) , int(p[6][:-1]) ,int(p[8][:-1]) ,int(p[8][:-1]) , int(p[10])))

    val = 0
    for a in range(0,101):
        for b in range(0,101-a):
            for c in range(0,101-a-b):
                d = 100 -a -b -c
                cap = max(0 , a*ing[0][0] + b*ing[1][0] + c*ing[2][0] + d*ing[3][0])
                dur = max(0 , a*ing[0][1] + b*ing[1][1] + c*ing[2][1] + d*ing[3][1])
                fla = max(0 , a*ing[0][2] + b*ing[1][2] + c*ing[2][2] + d*ing[3][2])
                tex = max(0 , a*ing[0][3] + b*ing[1][3] + c*ing[2][3] + d*ing[3][3])
                
                tmp = cap * dur * fla * tex

                if tmp > val : val = tmp

    print(val)
     

@profiler
def part2():

    ing = []

    with open('input.txt') as f:
        for l in f:
            p = l.strip().split()
            ing.append((int(p[2][:-1]) ,int(p[4][:-1]) , int(p[6][:-1]) ,int(p[8][:-1]) , int(p[10])))

    val = 0

    for a in range(0,101):
        for b in range(0,101-a):
            for c in range(0,101-a-b):
                d = 100 -a -b -c
                if (a*ing[0][4] + b*ing[1][4] + c*ing[2][4] + d*ing[3][4]) == 500 :
                    cap = max(0 , a*ing[0][0] + b*ing[1][0] + c*ing[2][0] + d*ing[3][0])
                    dur = max(0 , a*ing[0][1] + b*ing[1][1] + c*ing[2][1] + d*ing[3][1])
                    fla = max(0 , a*ing[0][2] + b*ing[1][2] + c*ing[2][2] + d*ing[3][2])
                    tex = max(0 , a*ing[0][3] + b*ing[1][3] + c*ing[2][3] + d*ing[3][3])
                
                    tmp = cap * dur * fla * tex
                    if tmp > val : val = tmp

    print(val)


if __name__ == "__main__":

    part1()
    part2()
