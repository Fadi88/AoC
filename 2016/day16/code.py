import time
import re
import hashlib
import sys


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print('Method ' + method.__name__ + ' took : ' +
              "{:2.5f}".format(time.time()-t) + ' sec')
        return ret
    return wrapper_method


@profiler
def part1():
    inp = '00111101111101000'
    trg_len = 272

    while len(inp) < trg_len:
        b = inp[::-1]
        b = b.replace('0', 'x').replace('1', '0').replace('x', '1')
        inp = inp + '0' + b

    inp = inp[:trg_len]
    
    check_sum = ''

    while len(check_sum) % 2 == 0:
        if check_sum == '':
            check_sum = inp

        tmp = []
        for i in range(0,len(check_sum),2):
            tmp.append('1' if check_sum[i] == check_sum[i+1] else '0')

        check_sum = ''.join(tmp)

    print(check_sum)


@profiler
def part2():
    inp = '00111101111101000'
    trg_len = 35651584


    while len(inp) < trg_len:
        b = inp[::-1]
        b = b.replace('0', 'x').replace('1', '0').replace('x', '1')
        inp = inp + '0' + b

    inp = inp[:trg_len]
    
    check_sum = ''

    while len(check_sum) % 2 == 0:
        if check_sum == '':
            check_sum = inp

        tmp = []
        for i in range(0,len(check_sum),2):
            tmp.append('1' if check_sum[i] == check_sum[i+1] else '0')

        check_sum = ''.join(tmp)

    print(check_sum)


if __name__ == "__main__":

    part1()
    part2()
