import time,os
from collections import defaultdict
import hashlib 

def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        method(*arg, **kw)
        print('Method '  + method.__name__ +' took : ' + "{:2.5f}".format(time.time()-t) + ' sec')
    return wrapper_method

@profiler
def part1():
  
    with open('input.txt', 'r') as f_in :
        l = f_in.read().strip()
        val = 0
        while True:
            st = 'yzbqklnj' + str(val)
            hash = hashlib.md5(bytes(st,'utf-8')).hexdigest()
            if hash[0] == hash[1] == hash[2] == hash[3] == hash[4] == '0':
                print(val)
                break
            val += 1
            

@profiler
def part2():

    with open('input.txt', 'r') as f_in :
        l = f_in.read().strip()
        val = 0
        while True:
            st = 'yzbqklnj' + str(val)
            hash = hashlib.md5(bytes(st,'utf-8')).hexdigest()
            if hash[0] == hash[1] == hash[2] == hash[3] == hash[4] == hash[5] == '0':
                print(val)
                break
            val += 1



if __name__ == "__main__":

    part1()
    part2()
