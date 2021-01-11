import time
import os
import hashlib
from collections import Counter


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        method(*arg, **kw)
        print('Method ' + method.__name__ + ' took : ' +
              "{:2.5f}".format(time.time()-t) + ' sec')
    return wrapper_method


@profiler
def part1():

    inp = 'abbhdwsy'

    code = []
    inc = 1

    while len(code) < 8:
        tmp = inp + str(inc)
        hash = hashlib.md5(bytes(tmp, 'utf-8')).hexdigest()
        if hash[0] == hash[1] == hash[2] == hash[3] == hash[4] == '0':
            code.append(hash[5])

        inc += 1

    print(''.join(code))

@profiler
def part2():

    inp = 'abbhdwsy'

    code = ['-'] * 8
    inc = 1

    while code.count('-') > 0:
        tmp = inp + str(inc)
        hash = hashlib.md5(bytes(tmp, 'utf-8')).hexdigest()
        if hash[0] == hash[1] == hash[2] == hash[3] == hash[4] == '0':
            if int(hash[5],16) < 8:
                if code[int(hash[5],16)] == '-':
                    code[int(hash[5],16)] = hash[6]

        inc += 1

    print(''.join(code))


if __name__ == "__main__":

    part1()
    part2()
