import time,os
import re

def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        method(*arg, **kw)
        print('Method '  + method.__name__ +' took : ' + "{:2.5f}".format(time.time()-t) + ' sec')
    return wrapper_method

@profiler
def part1():

    cnt = 0
    with open('input.txt', 'r') as f_in:
        for l in f_in:
            lim = re.findall(r'\d+' , l)
            ch = l [l.find(':') - 1]
            password = l [l.find(':') +1:].strip()
            if  int(lim[0]) <= password.count(ch)  and password.count(ch) <= int(lim[1]):
                cnt += 1
        print("part 1 answer : " ,cnt)
    

@profiler
def part2():
    with open('input.txt', 'r') as f_in:
        cnt = 0
    with open('input.txt', 'r') as f_in:
        for l in f_in:
            pos = re.findall(r'\d+' , l)
            ch = l [l.find(':') - 1]
            password = l [l.find(':') +1:].strip()
            min = False
            max = False

            if  int(pos[0])  <= len(password):
                min = password[int(pos[0]) - 1] == ch

            if  int(pos[1])  <= len(password):
                max = password[int(pos[1]) - 1] == ch

            if min != max:
                cnt += 1
        print("part 2 answer : " ,cnt)

if __name__ == "__main__":
    

    part1()
    part2()
