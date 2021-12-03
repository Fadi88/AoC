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
def part1():
    nums = [l.strip() for l in open("input.txt")]

    gamma = list(nums[0])
    epsilon = list(nums[0])

    for bit in range(len(nums[0])):
        bits = [l[bit] for l in nums]

        if bits.count('1') > bits.count('0'):
            gamma[bit] = '1'
            epsilon[bit] = '0'
        else:
            gamma[bit] = '0'
            epsilon[bit] = '1'

    print("part 1 : ", int(''.join(gamma), 2) * int(''.join(epsilon), 2))


@profiler
def part2():

    nums_oxy = [l.strip() for l in open("input.txt")]
    nums_car = nums_oxy.copy()

    for bit in range(len(nums_oxy[0])):

        bits_oxy = [l[bit] for l in nums_oxy]

        if bits_oxy.count('1') >= bits_oxy.count('0'):
            nums_oxy = [l for l in nums_oxy if l[bit] == '1']
        else:
            nums_oxy = [l for l in nums_oxy if l[bit] == '0']

        if len(nums_oxy) == 1:
            break

    for bit in range(len(nums_car[0])):

        bits_car = [l[bit] for l in nums_car]

        if bits_car.count('1') >= bits_car.count('0'):
            nums_car = [l for l in nums_car if l[bit] == '0']
        else:
            nums_car = [l for l in nums_car if l[bit] == '1']

        if len(nums_car) == 1:
            break

    print("part 2 : ", int(nums_oxy[0], 2) * int(nums_car[0], 2))


if __name__ == "__main__":

    part1()
    part2()