import time,os
import re
from modint import chinese_remainder

def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print('Method '  + method.__name__ +' took : ' + "{:2.5f}".format(time.time()-t) + ' sec')
        return ret
    return wrapper_method

@profiler
def part1():

    l =  open('input.txt', 'r').read().split('\n')

    bound = int(l[0])
    ids = list(map(int , re.findall(r'\d+' , l[1])))
    delay = bound
    chosen_bus = 0

    for bus in ids:
        n_dep = bound // bus + 1
        if (n_dep*bus - bound) < delay :
            delay =  n_dep*bus - bound
            chosen_bus = bus

    print(chosen_bus*delay)

@profiler
def part2():
    l =  open('input.txt', 'r').read().split('\n')

    l = l[1].split(',')

    sched = []
    for idx,bus in enumerate(l):
        if bus == 'x':
            continue
        sched.append((int(bus) , idx))
    '''
    st_n = 760000000000000 // sched[0][0] + 1 
           
    for i in range(10000000000,11000000000):
        found = True
        for ele in sched[1:] :
            if ((st_n + i) * sched[0][0] + ele[1]) % ele[0] != 0 :
                found = False
                break

        if found :
            print( i , (st_n + i) * sched[0][0])
            break
    '''

    ids  = []
    rems = []

    for ele in sched:
        ids.append(ele[0])
        rems.append( -ele[1] % ele[0])

    print(chinese_remainder(ids,rems))
    answer = sched[0][0]
    inc    = sched[0][0]

    
    for ele in sched[1:]:
        found = False
        while not found:

            answer += inc

            if (answer + ele[1]) % ele[0] == 0:
                found = True

        inc *= ele[0]

    print(answer)

          
if __name__ == "__main__":

    part1()
    part2()
