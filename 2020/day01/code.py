import time,os

def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        method(*arg, **kw)
        print('Method '  + method.__name__ +' took : ' + "{:2.5f}".format(time.time()-t) + ' sec')
    return wrapper_method

target_val = 2020

@profiler
def part1():
  
    ls = None

    with open('input.txt', 'r') as f_in :
        ls = [int(l) for l in f_in]

    for i in range(len(ls)):
        if target_val - ls[i] in ls:
            print("answer part 1 : " + str(ls[i] * ( target_val - ls[i])))
            return




@profiler
def part2():

    ls = None

    with open('input.txt', 'r') as f_in :
        ls = [int(l) for l in f_in]

    for a in range(len(ls)):
        for b in range(len(ls)):
            if a == b :
                continue
            tmp_sum = ls[a] + ls[b]

            if target_val - tmp_sum in ls:
                print("answer part 2 : " + str(ls[a] * ls[b] * (target_val - tmp_sum)))
                return

if __name__ == "__main__":

    part1()
    part2()

    
    