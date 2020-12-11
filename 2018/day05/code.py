import time,os,re
from collections import defaultdict

def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print('Method '  + method.__name__ +' took : ' + "{:2.5f}".format(time.time()-t) + ' sec')
        return ret
    return wrapper_method

@profiler
def part1():
   
    st = open('input.txt').read().strip()
    
    while True:
        tmp = st
        for i in range(26):
            tr = str(chr(ord('a') + i) + chr(ord('A') + i))
            tmp = tmp.replace(tr , ''  )
            tmp = tmp.replace(tr[::-1] , ''  )
        if tmp == st :
            break
        st = tmp
    print(len(st))
        

    

@profiler
def part2():

    input = open('input.txt').read().strip()
    ls = []

    for ch in range(26):

        st = input
        st = st.replace(chr(ord('a') + ch)  , '')
        st = st.replace(chr(ord('A') + ch) , '')


        while True:
            tmp = st
            for i in range(26):
                tr = str(chr(ord('a') + i) + chr(ord('A') + i))
                tmp = tmp.replace(tr , ''  )
                tmp = tmp.replace(tr[::-1] , ''  )
            if tmp == st :
                break
            st = tmp
        ls.append(len(st))
    print(min(ls))



if __name__ == "__main__":

    part1()
    part2()
