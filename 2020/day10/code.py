import time,os
from collections import defaultdict

def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret =method(*arg, **kw)
        print('Method '  + method.__name__ +' took : ' + "{:2.5f}".format(time.time()-t) + ' sec')
        return ret
    return wrapper_method

@profiler
def part1():

    l =  [int(tmp.strip()) for tmp in open('input.txt', 'r').readlines()]

    l.append(0)
    l.append(max(l) + 3)
    l.sort()


    d1 = 0 
    d3 = 0

    for i in range(1, len(l)):
        if l[i] - l[i - 1 ] == 1:
            d1 +=1
        elif l[i] - l[i - 1 ] == 3 :
            d3 += 1
        else :
            print(l[i] - l[i - 1 ])

    print('part 1 answer : ' , d1*d3)
    

@profiler
def part2():

    l =  [int(tmp.strip()) for tmp in open('input.txt', 'r').readlines()]

    dev = max(l) + 3

    l.append(0)
    l.sort()

    comb = defaultdict(lambda : 0)

    comb[dev] = 1
    
    for v in l[::-1]:
        comb[v] = comb[v+1] + comb[v+2] + comb[v+3]
        #print(v , comb[v])

    print("Part 2 answer :", comb[0])

if __name__ == "__main__":

    part1()
    part2()
