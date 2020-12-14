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

    mask = ''
    mem  = {}

    for l in  open('input.txt', 'r').readlines():
        l = l.strip()

        if 'mask' in l :
            mask = l.replace('mask = ','')

        else :
            nums = re.findall(r'\d+', l)
            
            loc = int(nums[0])
            val = '{:036b}'.format(int(nums[1]))

            for idx,ch in enumerate(mask):
                if ch != 'X':
                    val = val[:idx] + ch + val[idx+1:]
            mem[loc] = int(val,2)

    print(sum(mem.values()))

@profiler
def part2():

    mask = ''
    mem  = {}

    for l in  open('input.txt', 'r').readlines():
        l = l.strip()

        if 'mask' in l :
            mask = l.replace('mask = ','')

        else :
            nums = re.findall(r'\d+', l)

            loc = int(nums[0])
            val = int(nums[1])

            base_loc = loc | int(mask.replace('X' , '0'),2)

            
            xs = mask.count('X')
            x_loc = [i for i, ltr in enumerate(mask) if ltr == 'X']

            for i in map(lambda tmp : bin(tmp)[2:].zfill(xs),range(2**xs)):
                mod_loc = list(bin(base_loc)[2:].zfill(36))
                assert len(x_loc) == len(i)
                for idx , dig in zip(x_loc,i):
                    mod_loc[idx] = dig
                mem[int(''.join(mod_loc) , 2)] = val

    print(sum(mem.values()))

if __name__ == "__main__": 

    part1()
    part2()
