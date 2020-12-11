import time,os

def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        method(*arg, **kw)
        print('Method '  + method.__name__ +' took : ' + "{:2.5f}".format(time.time()-t) + ' sec')
    return wrapper_method

@profiler
def part1():
    ls = []
    with open('input.txt', 'r') as f_in:
        for l in f_in:
            ls.append(l.strip())


        for l in ls:
            print(l)
    

@profiler
def part2():
    with open('input.txt', 'r') as f_in:
        pass

if __name__ == "__main__":
    

    part1()
    part2()

    
    