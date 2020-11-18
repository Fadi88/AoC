import time,os

def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        method(*arg, **kw)
        print('Method '  + method.__name__ +' took : ' + "{:2.5f}".format(time.time()-t) + ' sec')
    return wrapper_method

@profiler
def part1(fin):
    pass

@profiler
def part2(fin):
    pass

if __name__ == "__main__":
    f_in = open('input.txt', 'r')

    part1(f_in)
    part2(f_in)

    f_in.close()
    