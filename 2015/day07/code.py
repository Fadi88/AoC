import time,os,re
from collections import defaultdict

def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print('Method '  + method.__name__ +' took : ' + "{:2.5f}".format(time.time()-t) + ' sec')
        return ret
    return wrapper_method

cache = {}

def eval_sig(table,sig):

    global cache

    if sig in cache : return cache[sig]

    if sig in table:
        if 'AND' in table[sig]:
            p = table[sig].split(' AND ')
            res = (eval_sig(table,p[0]) & eval_sig(table,p[1])) & 0xffff
            cache[sig] = res
            return res
        elif 'OR' in table[sig]:
            p = table[sig].split(' OR ')
            res = (eval_sig(table,p[0]) | eval_sig(table,p[1])) & 0xffff
            cache[sig] = res
            return res
        elif 'RSHIFT' in table[sig]:
            p = table[sig].split(' RSHIFT ')
            res = eval_sig(table,p[0]) >> int(p[1])
            cache[res] = cache
            return res
        elif 'LSHIFT' in table[sig]:
            p = table[sig].split(' LSHIFT ')
            res = eval_sig(table,p[0]) << int(p[1])
            cache[res] = cache
            return res
        elif 'NOT' in table[sig]:
            p = table[sig].split()
            res = (~eval_sig(table,p[1])) & 0xffff
            cache[res] = cache
            return res
        else:
            res = eval_sig(table,table[sig])
            cache[res] = cache
            return res
    else :
        res = int(sig)
        cache[sig] = res
        return res


@profiler
def part1():
    table = {}
    with open('input.txt', 'r') as f:
        for l in f:
            p = l.strip().split('->')
            table[p[1].strip()] = p[0].strip()

    print(eval_sig(table,'a'))

            

@profiler
def part2():

    table = {}
    global cache
    cache = {}
    with open('input.txt', 'r') as f:
        for l in f:
            p = l.strip().split('->')
            table[p[1].strip()] = p[0].strip()

    table['b'] = str(eval_sig(table,'a'))
    cache = {}
    print(eval_sig(table,'a'))

if __name__ == "__main__":

    part1()
    part2()
