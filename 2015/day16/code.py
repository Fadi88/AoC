import time,re
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

    inp = []

    with open('input.txt') as f:
        for l in f:
            p = l.strip().split()
            inp.append({p[2][:-1] : int(p[3][:-1]) ,p[4][:-1] : int(p[5][:-1]) , p[6][:-1] : int(p[7]) })

    for i in range(len(inp)):
        aunt = inp[i]
        is_valid = True
        if 'children' in aunt :
            is_valid &= aunt['children'] == 3
        if 'cats' in aunt :
            is_valid &= aunt['cats'] == 7
        if 'samoyeds' in aunt :
            is_valid &= aunt['samoyeds'] == 2
        if 'pomeranians' in aunt :
            is_valid &= aunt['pomeranians'] == 3
        if 'akitas' in aunt :
            is_valid &= aunt['akitas'] == 0
        if 'vizslas' in aunt :
            is_valid &= aunt['vizslas'] == 0
        if 'goldfish' in aunt :
            is_valid &= aunt['goldfish'] == 5
        if 'trees' in aunt :
            is_valid &= aunt['trees'] == 3
        if 'cars' in aunt :
            is_valid &= aunt['cars'] == 2
        if 'perfumes' in aunt :
            is_valid &= aunt['perfumes'] == 1

        if is_valid : 
            print(i+1)
            break
        



@profiler
def part2():

    inp = []

    with open('input.txt') as f:
        for l in f:
            p = l.strip().split()
            inp.append({p[2][:-1] : int(p[3][:-1]) ,p[4][:-1] : int(p[5][:-1]) , p[6][:-1] : int(p[7]) })

    for i in range(len(inp)):
        aunt = inp[i]
        is_valid = True
        if 'children' in aunt :
            is_valid &= aunt['children'] == 3
        if 'cats' in aunt :
            is_valid &= aunt['cats'] > 7
        if 'samoyeds' in aunt :
            is_valid &= aunt['samoyeds'] == 2
        if 'pomeranians' in aunt :
            is_valid &= aunt['pomeranians'] < 3
        if 'akitas' in aunt :
            is_valid &= aunt['akitas'] == 0
        if 'vizslas' in aunt :
            is_valid &= aunt['vizslas'] == 0
        if 'goldfish' in aunt :
            is_valid &= aunt['goldfish'] < 5
        if 'trees' in aunt :
            is_valid &= aunt['trees'] > 3
        if 'cars' in aunt :
            is_valid &= aunt['cars'] == 2
        if 'perfumes' in aunt :
            is_valid &= aunt['perfumes'] == 1

        if is_valid : 
            print(i+1)
            break
           


if __name__ == "__main__":

    part1()
    part2()
