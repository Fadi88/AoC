import time,os,re
from collections import defaultdict

def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        method(*arg, **kw)
        print('Method '  + method.__name__ +' took : ' + "{:2.5f}".format(time.time()-t) + ' sec')
    return wrapper_method

@profiler
def part1():

    with open('input.txt', 'r') as f_in:
        area = defaultdict(lambda : 0)

        for l in f_in:
            cid,x,y,w,h = map(int,re.findall(r'\d+' , l))
            for dx in range(x,x+w):
                for dy in range(y,y+h):
                  area[(dx,dy)] += 1


        print(min(area.values()))
        print(len(list(filter( lambda x : x > 1 , area.values()))))
    

@profiler
def part2():
    area = defaultdict(lambda :0)

    with open('input.txt', 'r') as f_in:
        
        for l in f_in:
            cid,x,y,w,h = map(int,re.findall(r'\d+' , l))
            for dx in range(x,x+w):
                for dy in range(y,y+h):
                  area[(dx,dy)] += 1

    with open('input.txt', 'r') as f_in:
        for l in f_in:
            cid,x,y,w,h = map(int,re.findall(r'\d+' , l))
            overlap = False
            for dx in range(x,x+w):
                if overlap:
                        break
                for dy in range(y,y+h):
                    if area[(dx,dy)] > 1 :
                        overlap = True
                        break
            if not overlap:
                print(cid)
                break


if __name__ == "__main__":

    part1()
    part2()
  