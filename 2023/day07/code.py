from time import perf_counter
from collections import Counter
import heapq  

def profiler(method):
    def wrapper_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print('Method ' + method.__name__ + ' took : ' +
              "{:2.5f}".format(perf_counter()-t) + ' sec')
        return ret
    return wrapper_method

ranks = "AKQJT98765432"
class Hand:
    def __init__(self,h):
        self.h = h
        self.c = Counter(h)

    def __repr__(self) -> str:
        return self.h

    def __gt__(self,other) :
        if len(self.c) != len(other.c):
            return len(self.c) < len(other.c)
        if len(self.c.values()) == 2 and len(set(list(self.c.values())+list(other.c.values()))) == 4: # full house vs 4 of a kind
            return 4 in self.c.values()
        if len(self.c.values()) == 3 and len(set(list(self.c.values())+list(other.c.values()))) == 3: # 2 pairs vs 3 of a kind
            return 3 in self.c.values()
        for c_h,o_h in zip(self.h,other.h):
            if c_h != o_h:
                return ranks.index(c_h) < ranks.index(o_h)
        return False

@profiler
def part1():
    bids = {}

    for l in open("day07/input.txt"):
        p = l.split()
        bids[Hand(p[0])] = int(p[1])
        
    l = list(bids.keys())
    l.sort()

    total = 0
    for i,h in enumerate(l):
        total += (i+1) * bids[h]
    print(total)

ranks_2 = "AKQT98765432J"
def get_rank(o):
    match len(o):
        case 1:
            return 1
        case 2:
            return 2 if 4 in o.values() else 3
        case 3:
            return 4 if 3 in o.values() else 5
        case 4:
            return 6
        case 5:
            return 7

class Hand2:
    def __init__(self,h):
        self.h = h
        self.c = Counter(h)
        self.rank = min([get_rank(Counter(h.replace("J",test))) for test in "AKQT98765432"])
    
    def __repr__(self) -> str:
        return self.h

    def __lt__(self,other) :
        if self.rank != other.rank:
            return self.rank > other.rank
        for c_h,o_h in zip(self.h,other.h):
            if c_h != o_h:
                return ranks_2.index(c_h) > ranks_2.index(o_h)

        return False

@profiler
def part2():
    bids = {}

    for l in open("day07/input.txt"):
        p = l.split()
        bids[Hand2(p[0])] = int(p[1])
        
    l = list(bids.keys())
    l.sort()

    total = 0
    for i,h in enumerate(l):
        total += (i+1) * bids[h]
    print(total)


if __name__ == "__main__":

    part1()
    part2()