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

        elif dr == 'R':
            ang -= mag
   
        elif dr == 'L':
            ang += mag

        else :
            delta = {'N' : (0,+mag) , 'S' : (0,-mag) , 'E' : (mag,0) ,  'W' : (-mag,0)} 

            x += delta[dr][0]
            y += delta[dr][1]

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

        # source https://stackoverflow.com/a/3162731
        elif dr == 'R':
            nx =   wx * math.cos(math.radians(mag)) + wy * math.sin(math.radians(mag))
            ny =  -wx * math.sin(math.radians(mag)) + wy * math.cos(math.radians(mag))

            wx = round(nx)
            wy = round(ny)
 
        elif dr == 'L':
            nx =   wx * math.cos(-math.radians(mag)) + wy * math.sin(-math.radians(mag))
            ny =  -wx * math.sin(-math.radians(mag)) + wy * math.cos(-math.radians(mag))

            wx = round(nx)
            wy = round(ny)

        else :
            delta = {'N' : (0,+mag) , 'S' : (0,-mag) , 'E' : (mag,0) ,  'W' : (-mag,0)}

            wx += delta[dr][0]
            wy += delta[dr][1]
            
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

        elif dr == 'R':
            theta = np.radians(mag)
            Rt = np.array([[np.cos(theta) , -np.sin(theta)] , [np.sin(theta) , np.cos(theta)]])
            wp = np.rint(wp.dot(Rt)).astype(int)
 
        elif dr == 'L':
            theta = np.radians(-mag)
            Rt = np.array([[np.cos(theta) , -np.sin(theta)] , [np.sin(theta) , np.cos(theta)]])

            wp = np.rint(wp.dot(Rt)).astype(int)

        else :
            delta = {'N' : np.array([0,1]) , 'S' : np.array([0,-1]), 'E' : np.array([1,0]) ,  'W' : np.array([-1,0])}

            wp += mag * delta[dr]
            
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

        elif dr == 'R':
           wp *= 1j**(-mag/90)

        elif dr == 'L':
           wp *= 1j**(mag/90)
 
        else :
            delta = {'N' : 1j , 'S' : -1j, 'E' : 1 ,  'W' : -1}
            wp += mag * delta[dr]
            
    print('part 2 using complex answer : ' , int(abs(pos.real) +  abs(pos.imag)))

if __name__ == "__main__":

    part1()
    part2()
    p2_complex()
    p2_matrix()
    