import time,os

def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        method(*arg, **kw)
        print('Method '  + method.__name__ +' took : ' + "{:2.5f}".format(time.time()-t) + ' sec')
    return wrapper_method

@profiler
def part1():
  
    with open('input.txt', 'r') as f_in :
        ls = []
        for l in f_in:
            ls.append(int(l))

        for i in range(len(ls)):
            for t in range(len(ls)):
                if i == t :
                    continue
                if ls[i] + ls[t] == 2020:
                    print("answer part 1 : " + str(ls[i] * ls[t]) )
                    return




@profiler
def part2():
    with open('input.txt', 'r') as f_in :
        ls = []
        for l in f_in:
            ls.append(int(l))

        for a in range(len(ls)):
            for b in range(len(ls)):
                if a == b :
                    continue
                tmp_sum = ls[a] + ls[b]

                for c in range(len(ls)):
                    if c == b or c == a:
                        continue
                    if  tmp_sum + ls[c]== 2020:
                        print("answer part 2 : " + str(ls[a] * ls[b] * ls[c]) )
                        return

if __name__ == "__main__":

    part1()
    part2()

    
    