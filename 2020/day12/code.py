import time,os
import math
import numpy as np

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

            wx = round(nx)
            wy = round(ny)
 
        elif dr == 'L':
            nx =  wx * math.cos(-math.radians(mag)) + wy * math.sin(-math.radians(mag))
            ny =  -wx * math.sin(-math.radians(mag)) + wy * math.cos(-math.radians(mag))

            wx = round(nx)
            wy = round(ny)
            
    print('part 2 answer : ' , abs(x) +  abs(y))

@profiler
def p2_matrix():

    pos = np.array([0,0])

    wp  = np.array([10,1]) 

    for l in open('input.txt'):
        dr = l[0]
        mag = int(l.strip()[1:])

        if dr == 'F' :
            pos += mag * wp

        elif dr == 'N':
            wp += mag * np.array([0,1])

        elif dr == 'S':
            wp += mag * np.array([0,-1])

        elif dr == 'E':
            wp += mag * np.array([1,0])

        elif dr == 'W':
            wp += mag * np.array([-1,0])

        elif dr == 'R':
            theta = np.radians(mag)
            Rt = np.array([[np.cos(theta) , -np.sin(theta)] , [np.sin(theta) , np.cos(theta)]])
            wp = np.rint(wp.dot(Rt)).astype(int)
 
        elif dr == 'L':
            theta = np.radians(-mag)
            Rt = np.array([[np.cos(theta) , -np.sin(theta)] , [np.sin(theta) , np.cos(theta)]])

            wp = np.rint(wp.dot(Rt)).astype(int)
            
    print('part 2 using matrix answer : ' , np.abs(pos[0]) +  np.abs(pos[1]))


@profiler
def p2_complex():

    pos = 0 + 0j

    wp  = 10 + 1j

    for l in open('input.txt'):
        dr = l[0]
        mag = int(l.strip()[1:])

        if dr == 'F' :
            pos += mag * wp

        elif dr == 'N':
            wp += mag * 1j

        elif dr == 'S':
            wp -= mag * 1j

        elif dr == 'E':
            wp += mag * 1

        elif dr == 'W':
            wp -= mag * 1

        elif dr == 'R':
           wp *= 1j**(-mag/90)
 
        elif dr == 'L':
           wp *= 1j**(mag/90)
            
    print('part 2 using complex answer : ' , int(abs(pos.real) +  abs(pos.imag)))

if __name__ == "__main__":

    part1()
    part2()
    p2_complex()
    p2_matrix()
    