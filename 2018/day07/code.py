import time
from collections import defaultdict

def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print('Method ' + method.__name__ + ' took : ' +
              "{:2.5f}".format(time.time()-t) + ' sec')
        return ret
    return wrapper_method



@profiler
def both_part():
    workers_count = 5
    overhead = 60

    needs = defaultdict(set)
    letters = set()
    for l in open('input.txt'):
        needs[l[36]].add(l[5])
        letters |= set([l[36], l[5]])

    t = 0
    ret = ''
    time = {}
    workers = [None] * workers_count

    while len(ret) < len(letters):
        ready = []
        if workers.count(None) > 0:
            for l in letters:
                if len(needs[l]) == 0 and l not in ret and l not in workers:
                    ready.append(l)

            ready.sort()
            for _ in range(min(workers.count(None),len(ready))):
                ch = ready.pop(0)
                workers[workers.index(None)] = ch
                time[ch] = t

        t += 1

        for ele in workers:
            if ele is not None and t - time[ele] == overhead + ord(ele) - ord('A') + 1:
                ret += ele
                workers[workers.index(ele)] = None
                for tmp in needs:
                    needs[tmp] -= set(ele)

    print(ret , t)
                

if __name__ == "__main__":

    both_part()
