import os


for i in range(25):
    dir = "day" + "{:02d}".format(i+1)
    if not os.path.exists(dir):
        os.mkdir(dir)
    open(dir + "/input.txt", "w").close()
    f_code = open(dir + '/code.py' , 'w')

    f_code.write('''import time,os

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
    '''
    )

    f_code.close()