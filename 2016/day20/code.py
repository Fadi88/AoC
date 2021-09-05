import time


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

    r = []

    for l in open('input.txt').read().split('\n'):
        p = list(map(int, l.split('-')))
        r.append([p[0], p[1]])

    r.sort()

    for i in range(len(r) - 1):

        if r[i][1] > r[i+1][1]:
            r[i+1][1] = r[i][1]
        elif r[i+1][0] > r[i][1]:
            print(r[i][1]+1)
            break


@profiler
def part2():

    r = []

    for l in open('input.txt').read().split('\n'):
        p = list(map(int, l.split('-')))
        r.append([p[0], p[1]])

    r.sort()

    cnt = 0

    for i in range(len(r) - 1):

        if r[i][1] > r[i+1][1]:
            r[i+1][1] = r[i][1]
        elif r[i+1][0] > r[i][1]:
            cnt += (r[i+1][0] - r[i][1] - 1)

    print(cnt)


if __name__ == "__main__":

    part1()
    part2()
