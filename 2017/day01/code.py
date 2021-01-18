import time,os

def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        method(*arg, **kw)
        print('Method '  + method.__name__ +' took : ' + "{:2.5f}".format(time.time()-t) + ' sec')
    return wrapper_method

@profiler
def part1():
  
    
    inp = open('input.txt').read().strip()

    cnt = 0
    for i in range(len(inp)):
        if inp[i] == inp[(i+1)%len(inp)]:
            cnt += int(inp[i])

    print(cnt)
    
    

@profiler
def part2():

    inp = open('input.txt').read().strip()

    cnt = 0
    for i in range(len(inp)):
        if inp[i] == inp[(i+len(inp)//2)%len(inp)]:
            cnt += int(inp[i])

    print(cnt)

if __name__ == "__main__":

    part1()
    part2()
