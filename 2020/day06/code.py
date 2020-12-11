import time,os

def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        method(*arg, **kw)
        print('Method '  + method.__name__ +' took : ' + "{:2.5f}".format(time.time()-t) + ' sec')
    return wrapper_method

@profiler
def part1():

    with open('input.txt', 'r') as f_in:
        ls = [set(t.replace('\n' , '')) for t in f_in.read().split('\n\n')]
        
        cnt = 0
        for gr in ls :
            cnt += len(gr)
        print('part 1 answer : ' , cnt)
    

@profiler
def part2():
    with open('input.txt', 'r') as f_in:
        ls = f_in.read().split('\n\n')

        cnt = 0
        for gr in ls:
            indvs = gr.split('\n')
            tmp = set(indvs[0])

            for indv in indvs :
                tmp = tmp.intersection(indv)
            cnt += len(tmp)
            
        print('part 2 answer : ' , cnt)

if __name__ == "__main__":
    

    part1()
    part2()

    
    