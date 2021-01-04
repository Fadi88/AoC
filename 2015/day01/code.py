import time,os

def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        method(*arg, **kw)
        print('Method '  + method.__name__ +' took : ' + "{:2.5f}".format(time.time()-t) + ' sec')
    return wrapper_method

@profiler
def part1():
  
    with open('input.txt', 'r') as f_in :
        ls = f_in.read().strip()
        print(ls.count('(') - ls.count(')'))



@profiler
def part2():
    with open('input.txt', 'r') as f_in :
        ls = f_in.read().strip()
        floor = 0
        for idx,ch in enumerate(ls):
            if ch == '(' : floor += 1
            elif ch == ')' : floor -=1

            if floor == -1 : 
                print(idx + 1)
                break



if __name__ == "__main__":

    part1()
    part2()
