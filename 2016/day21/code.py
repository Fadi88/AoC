import time
from collections import deque


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print('Method ' + method.__name__ + ' took : ' +
              "{:2.5f}".format(time.time()-t) + ' sec')
        return ret
    return wrapper_method


def apply_steps(steps, inp):

    st = deque(inp)

    for l in steps:
        if 'swap position' in l:
            p = l.split()
            i1 = int(p[2])
            i2 = int(p[5])

            tmp = st[i1]
            st[i1] = st[i2]
            st[i2] = tmp

        elif 'swap letter' in l:
            p = l.split()
            e1 = p[2]
            e2 = p[5]

            tmp = st.index(e1)
            st[st.index(e2)] = e1
            st[tmp] = e2

        elif 'rotate based' in l:
            p = l.split()
            st.rotate(st.index(p[-1]) + (st.index(p[-1]) >= 4) + 1)
        elif 'rotate' in l:
            p = l.split()
            n = int(p[2])
            if 'right' in l:
                st.rotate(n)
            else:
                st.rotate(-n)

        elif 'reverse' in l:
            p = l.split()
            i1, i2 = int(p[2]), int(p[4])
            tmp = list(st)[i1:i2+1][::-1]

            for i in range(len(tmp)):
                st[i1+i] = tmp[i]

        elif 'move' in l:
            p = l.split()
            i1, i2 = int(p[2]), int(p[5])

            tmp = st[i1]
            del st[i1]

            st.insert(i2, tmp)

    return ''.join(st)


def apply_steps_reverse(steps, inp):

    st = deque(inp)

    rev_rot = {0: -9, 1: -1, 2: -6, 3: -2, 4: -7, 5: -3, 6: -8, 7: -4}
    for l in steps[::-1]:
        if 'swap position' in l:
            p = l.split()
            i1 = int(p[2])
            i2 = int(p[5])

            tmp = st[i1]
            st[i1] = st[i2]
            st[i2] = tmp

        elif 'swap letter' in l:
            p = l.split()
            e1 = p[2]
            e2 = p[5]

            tmp = st.index(e1)
            st[st.index(e2)] = e1
            st[tmp] = e2

        elif 'reverse' in l:
            p = l.split()
            i1, i2 = int(p[2]), int(p[4])
            tmp = list(st)[i1:i2+1][::-1]

            for i in range(len(tmp)):
                st[i1+i] = tmp[i]

        elif 'rotate left' in l or 'rotate right' in l:
            p = l.split()
            n = int(p[2])
            if 'right' in l:
                st.rotate(-n)
            else:
                st.rotate(n)

        elif 'move' in l:
            p = l.split()
            i2, i1 = int(p[2]), int(p[5])

            tmp = st[i1]
            del st[i1]

            st.insert(i2, tmp)

        elif 'rotate based' in l:
            p = l.split()
            st.rotate(rev_rot[st.index(p[-1])])

    return ''.join(st)


@profiler
def part1():

    print(apply_steps(open('input.txt').read().split('\n'), 'abcdefgh'))


@profiler
def part2():

    print(apply_steps_reverse(open('input.txt').read().split('\n'), 'fbgdceah'))


if __name__ == "__main__":

    part1()
    part2()
