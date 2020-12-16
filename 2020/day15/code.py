import time,os
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

    input = list(map(int, open('input.txt', 'r').read().split(',')))

    for _ in range(2020):
        if input.count(input[-1]) == 1 :
            input.append(0)
        else :
          idx = [i for i,num in enumerate(input) if num == input[-1]]
          input.append(idx[-1] - idx[-2])
        
    print(input[-1])
        

@profiler
def part2():

    input = list(map(int, open('input.txt', 'r').read().split(',')))

    age = defaultdict(list)

    for i in range(30000000):
        if len(input) == 0 :
            if len(age[mem]) < 2 :
                next = 0
            else :
                next = age[mem][-1] - age[mem][-2]
            age[next].append(i)
            mem = next

        else :
            mem = input.pop(0)
            age[mem].append(i)
            

    print(age.keys())
    print(mem)

@profiler
def part2_list():

    input = list(map(int, open('input.txt', 'r').read().split(',')))

    for _ in range(30000000):
        if input.count(input[-1]) == 1 :
            input.append(0)
        else :
          idx = [i for i,num in enumerate(input) if num == input[-1]]
          input.append(idx[-1] - idx[-2])
        
    print(input[30000000-1])
if __name__ == "__main__":

    part1()
    part2()
    #part2_list()
