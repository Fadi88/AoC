import time

def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print('Method ' + method.__name__ + ' took : ' +
              "{:2.5f}".format(time.time()-t) + ' sec')
        return ret
    return wrapper_method


def get_meta_sum(l):
    child_cnt = l.pop(0)
    meta_cnt  = l.pop(0)

    return  sum(get_meta_sum(l) for _ in range(child_cnt)) + sum(l.pop(0) for _ in range(meta_cnt))

def get_meta_val(l):
    child_cnt = l.pop(0)
    meta_cnt  = l.pop(0)

    childs_val = [get_meta_val(l) for _ in range(child_cnt)]
    metas  =  [l.pop(0) for _ in range(meta_cnt)]

    if child_cnt == 0 :
        ret = sum(metas)
    else :
        ret = 0
        for i in metas :
            if i-1 < child_cnt:
                ret += childs_val[i-1]

    return ret

@profiler
def part_1():
    d = list(map(int,open('input.txt').read().split()))
    print(get_meta_sum(d))

@profiler
def part_2():
    d = list(map(int,open('input.txt').read().split()))
    print(get_meta_val(d))
    

if __name__ == "__main__":

    part_1()
    part_2()
