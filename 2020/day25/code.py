import time,os,re
from copy import deepcopy

def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print('Method '  + method.__name__ +' took : ' + "{:2.5f}".format(time.time()-t) + ' sec')
        return ret
    return wrapper_method

def get_loop_size(subject_num , pub_key):
    loop_size = 0
    val = 1
    while val != pub_key:
        loop_size += 1
        val *= subject_num
        val %= 20201227
    return loop_size

def get_encryption_key(loop_size,subject_num):
    val = 1
    for _ in range(loop_size):
        val *= subject_num
        val %= 20201227
    return val
        

@profiler
def part1():
    d = 15335876
    c = 15086442

    c_loop_size = get_loop_size(7,c)
    d_loop_size = get_loop_size(7,d)

    enc_c = get_encryption_key(c_loop_size , d)
    enc_d = get_encryption_key(d_loop_size , c)

    assert enc_d == enc_d
    print(enc_c)

if __name__ == "__main__":
    
    part1()