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
    input = [int(i) for i in open("day06/input.txt").read().split(',')]

    for _ in range(80):
        tmp = []
        for i in input:
            if i == 0:
                tmp.append(8)
                tmp.append(6)
            else:
                tmp.append(i-1)

        input = tmp

    print(len(tmp))


@profiler
def part2():

    input = [int(i) for i in open("day06/input.txt").read().split(',')]

    ages = {i: 0 for i in range(9)}

    for age in input:
        ages[age] += 1

    for _ in range(256):
        new_ages = {i: 0 for i in range(9)}
        for age in ages:
            if age == 0:
                new_ages[8] += ages[0]
                new_ages[6] += ages[0]
            else:
                new_ages[age-1] += ages[age]

        ages = new_ages

    print(sum(ages.values()))


if __name__ == "__main__":

    part1()
    part2()
