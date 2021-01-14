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


def josephus(n, k):
    r = 0
    for i in range(1, n+1):
        r = (r+k) % i
    return r


@profiler
def part1():

    inp = 3017957

    print(josephus(inp, 2))


@profiler
def part2():

    inp = 3017957

    q1 = deque()
    q2 = deque()

    for i in range(1, inp+1):
        if i <= inp/2:
            q1.append(i)
        else:
            q2.append(i)

    while len(q1) + len(q2) != 1:

        a = q1.popleft()

        if len(q1) == len(q2):
            q1.pop()
        else:
            q2.popleft()

        q2.append(a)

        q1.append(q2.popleft())

    print(q1.pop())


if __name__ == "__main__":

    part1()
    part2()
