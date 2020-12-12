import time,os
import math

def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        method(*arg, **kw)
        print('Method '  + method.__name__ +' took : ' + "{:2.5f}".format(time.time()-t) + ' sec')
    return wrapper_method

@profiler
def part1():

    x = 0
    y = 0

    ang = 0

    for l in open('input.txt', 'r'):
        dr = l[0]
        mag = int(l.strip()[1:])
        if dr == 'F' :
            x += mag * math.cos(math.radians(ang))
            y += mag * math.sin(math.radians(ang))

        elif dr == 'N':
            y += mag

        elif dr == 'S':
            y -= mag

        elif dr == 'E':
            x += mag

        elif dr == 'W':
            x -= mag

        elif dr == 'R':
            ang -= mag
   
        elif dr == 'L':
            ang += mag

    print('part 1 answer : ' , int(abs(x) +  abs(y)))

@profiler
def part2():

    x = 0
    y = 0

    wx = 10
    wy = 1 

    for l in open('input.txt'):
        dr = l[0]
        mag = int(l.strip()[1:])

        if dr == 'F' :
            x += mag * wx
            y += mag * wy

        elif dr == 'N':
            wy += mag

        elif dr == 'S':
            wy -= mag

        elif dr == 'E':
            wx += mag

        elif dr == 'W':
            wx -= mag

        # source https://stackoverflow.com/a/3162731
        elif dr == 'R':
            nx =  wx * math.cos(math.radians(mag)) + wy * math.sin(math.radians(mag))
            ny =  -wx * math.sin(math.radians(mag)) + wy * math.cos(math.radians(mag))

            wx = int(round(nx))
            wy = int(round(ny))
 
        elif dr == 'L':
            nx =  wx * math.cos(-math.radians(mag)) + wy * math.sin(-math.radians(mag))
            ny =  -wx * math.sin(-math.radians(mag)) + wy * math.cos(-math.radians(mag))

            wx = int(round(nx))
            wy = int(round(ny))
            
    print('part 2 answer : ' , abs(x) +  abs(y))

if __name__ == "__main__":

    part1()
    part2()
