import time,os,re

def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        method(*arg, **kw)
        print('Method '  + method.__name__ +' took : ' + "{:2.5f}".format(time.time()-t) + ' sec')
    return wrapper_method

def eval_p1(inp) :
    while '*' in inp or '+' in inp :
        grp = re.findall(r'\d+[+*]\d+', inp)
        inp = inp.replace(grp[0] , str(eval(grp[0])) , 1)
    return inp

@profiler
def part1():
    sum = 0
    for l in open('input.txt', 'r').read().split('\n'):
        l = l.replace(' ' , '')
        while re.findall(r'(\([\d+*]+\))' , l) :
            grp = re.findall(r'(\([\d+*]+\))' , l)
            for par in grp:
                l = l.replace(par, eval_p1(par[1:-1]))
        sum += int(eval_p1(l))
    print(sum)
    
def eval_p2(inp) :
    while '+' in inp :
        grp = re.findall(r'\d+[\+]\d+', inp)
        inp = inp.replace(grp[0] , str(eval(grp[0])) , 1)
    return str(eval(inp))

@profiler
def part2():
    sum = 0
    for l in open('input.txt', 'r').read().split('\n'):
        l = l.replace(' ' , '')
        while re.findall(r'(\([\d+*]+\))' , l) :
            grp = re.findall(r'(\([\d+*]+\))' , l)
            for par in grp:
                l = l.replace(par, eval_p2(par[1:-1]))
        sum += int(eval_p2(l))
    print(sum)

if __name__ == "__main__":
    part1()
    part2()
