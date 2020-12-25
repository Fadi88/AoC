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
    return pow(subject_num , loop_size , 20201227)

@profiler
def part1():
    card_pub_key = 15335876
    door_pub_key = 15086442

    door_loop_size = get_loop_size(7,door_pub_key)
    card_loop_size = get_loop_size(7,card_pub_key)

    encryp_door = get_encryption_key(door_loop_size , card_pub_key)
    encryp_card = get_encryption_key(card_loop_size , door_pub_key)

    assert encryp_card == encryp_door
    print(encryp_card)

if __name__ == "__main__":
    
    part1()