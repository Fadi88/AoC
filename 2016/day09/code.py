import time
import os
import re


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print('Method ' + method.__name__ + ' took : ' +
              "{:2.5f}".format(time.time()-t) + ' sec')
        return ret
    return wrapper_method


@profiler
def part1():
    st = open('input.txt').read().strip()

    while '(' in st:
        p = re.findall(r'\(\d+x\d+\)', st)
        p_pos = st.find(p[0])
        l, rep = list(map(int, p[0][1:-1].split('x')))
        new_st = st[p_pos+len(p[0]):p_pos+l+len(p[0])
                    ].replace('(', '[').replace(')', ']')
        st = st.replace(st[p_pos:p_pos+l+len(p[0])], new_st * rep)

    print(len(st))


def get_size(st):

    if '(' not in st:
        return len(st)
    p = re.findall(r'\(\d+x\d+\)', st)
    p_pos = st.find(p[0])
    l, rep = list(map(int, p[0][1:-1].split('x')))
    return len(st[:p_pos]) + get_size(st[p_pos+len(p[0]):p_pos+len(p[0])+l]) * rep + get_size(st[p_pos+len(p[0])+l:])


@profiler
def part2():
    print(get_size(open('input.txt').read().strip()))


if __name__ == "__main__":

    part1()
    part2()
