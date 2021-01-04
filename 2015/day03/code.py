import time,os
from collections import defaultdict

def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        method(*arg, **kw)
        print('Method '  + method.__name__ +' took : ' + "{:2.5f}".format(time.time()-t) + ' sec')
    return wrapper_method

@profiler
def part1():
  
    moves = {'^' : 1j , 'v' : -1j , '<' : -1 , '>' : 1}
    with open('input.txt', 'r') as f_in :
        l = f_in.read().strip()
        pt = 0 + 0j
        houses = defaultdict(int)
        houses[pt] = 1
        for d in l:
            pt += moves[d]
            houses[pt] += 1

        print(len(houses))

@profiler
def part2():
    moves = {'^' : 1j , 'v' : -1j , '<' : -1 , '>' : 1}
    with open('input.txt', 'r') as f_in :
        l = f_in.read().strip()
        pt_s = 0 + 0j
        pt_r = pt_s
        houses = defaultdict(int)
        houses[pt_s] = 1
        for d in range(len(l) // 2):
            pt_s += moves[l[2*d]]
            pt_r += moves[l[2*d+1]]

            houses[pt_s] += 1
            houses[pt_r] += 1

        print(len(houses))


if __name__ == "__main__":

    part1()
    part2()
