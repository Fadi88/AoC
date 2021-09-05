import time,re
import json

def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print('Method '  + method.__name__ +' took : ' + "{:2.5f}".format(time.time()-t) + ' sec')
        return ret
    return wrapper_method

@profiler
def part1():

    with open('input.txt') as f:
        data = f.read()
    
    nums = list(map(int,re.findall(r'-?\d+' , data)))
    print(sum(nums))



def sum_recursive(data):
    if isinstance(data,int):
        return data
    elif isinstance(data,list):
        return sum([sum_recursive(d) for d in data])
    elif isinstance(data,str):
        return 0
    elif isinstance(data,dict):
        if 'red' in data.values():
            return 0
        else :
            return sum([sum_recursive(data[d]) for d in data])

@profiler
def part2():

    with open('input.txt') as f:
        data = json.load(f)

    print(sum_recursive(data))

if __name__ == "__main__":

    part1()
    part2()
