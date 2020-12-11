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
    ls = []
    tracker = defaultdict(list)
    with open('input.txt', 'r') as f_in:
        for l in f_in:
            ls.append(l.strip())

        ls.sort()
        for l in ls:
            if '#' in l:
                guard = int(re.findall(r'#(\d+)' , l)[0])
            elif 'falls asleep' in l:
                beg = int(re.findall(r':(\d+)' , l)[0])
            elif 'wakes up' in l:
                end = int(re.findall(r':(\d+)' , l)[0])
                tracker[guard].append((beg , end))
        
    total_sleep = {}
    for guard in tracker:
        sum = 0
        for nap in tracker[guard]:
            sum += nap[1] - nap[0]
        total_sleep[guard] = sum

    max_sleep = max(total_sleep.values())
    chosen_1 = list(filter(lambda x:x[1] == max_sleep,total_sleep.items()))[0][0]
    
    hist = [0] * 60

    for nap in tracker[chosen_1]:
        for i in range(nap[0] , nap[1]):
            hist[i] += 1
        
    hi_pr = hist.index(max(hist))

    print(hi_pr * chosen_1)

    

@profiler
def part2():
    with open('input.txt', 'r') as f_in:
        pass

if __name__ == "__main__":
    

    part1()
    part2()

    
    