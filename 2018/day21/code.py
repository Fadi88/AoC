# pylint: disable=C0114, C0116, C0209

import time
import heapq

DEPTH = 10647
TARGET = (7, 770)

# DEPTH = 510
# TARGET = (10, 10)


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print("Method " + method.__name__ + " took : " + "{:2.5f}".format(time.time() - t) + " sec")
        return ret

    return wrapper_method

@profiler
def part_1():
    t = int(open("day21/input.txt","r").readlines()[8].split()[1])

    r = [0]*6
  
    while True:
        r[0] = r[2] | 65536
        r[2] = t

        while True:
            r[2] = (((r[2] + (r[0] & 255)) & 16777215) * 65899) & 16777215
            if 256 > r[0]:
                print(r[2])
                return
            else:
                r[0] //= 256


@profiler
def part_2():

    r = [0]*6
    r[5] = int(open("day21/input.txt","r").readlines()[8].split()[1])
    r2s = []

    while True:
        r[0] = r[2] | 65536
        r[2] = r[5]

        while True:
            # 255:10 , 16777215 :12 , 65899 : 13 , 16777215 : 14
            # assuming hard coded except for line 8
            r[2] = (((r[2] + (r[0] & 255)) & 16777215) * 65899) & 16777215  
            if 256 > r[0]:
                if r[2] in r2s: # loop starting
                    print(r2s[-1])
                    return
                else:
                    r2s.append(r[2])
                    break
            else:
                r[0] //= 256


if __name__ == "__main__":
    part_1()
    part_2()
