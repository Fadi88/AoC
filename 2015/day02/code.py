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
        area = 0
        for l in f_in:
            ls = list(map(int,l.strip().split('x')))
            ls.sort()
            area += 3*ls[0]*ls[1] + 2*ls[0]*ls[2] + 2*ls[1]*ls[2]

        print(area)

@profiler
def part2():
    with open('input.txt', 'r') as f_in :
        ribbon = 0
        for l in f_in:
            ls = list(map(int,l.strip().split('x')))
            ls.sort()
            ribbon += 2*ls[0] + 2*ls[1]
            ribbon += ls[0] * ls[1] * ls[2]

        print(ribbon)


if __name__ == "__main__":

    part1()
    part2()
