import time
import re
from collections import defaultdict
from itertools import combinations


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print('Method ' + method.__name__ + ' took : ' +
              "{:2.5f}".format(time.time()-t) + ' sec')
        return ret
    return wrapper_method


def battle(p1, p2):  # (hp,damage,armor)

    p1_hp = p1[0]
    p2_hp = p2[0]

    while p1_hp > 0 and p2_hp > 0:
        p2_hp -= max(1, p1[1] - p2[2])
        if p2_hp <= 0:
            break
        p1_hp -= max(1, p2[1] - p1[2])

    return p1_hp > 0


@profiler
def part1():

    with open('input.txt') as f:
        w, a, r = f.read().split('\n\n')

    w, a, r = w.split('\n')[1:], a.split('\n')[1:], r.split('\n')[1:]

    w = [(int(i.split()[1]), int(i.split()[2]), int(i.split()[3])) for i in w]
    a = [(int(i.split()[1]), int(i.split()[2]), int(i.split()[3])) for i in a]
    r = [(int(i.split()[2]), int(i.split()[3]), int(i.split()[4])) for i in r]

    a.append((0, 0, 0))  # no armor choice

    b = (100, 8, 2)  # input

    min_cost = 100000
    for curr_w in w:
        for curr_a in a:
            for ring_count in [0, 1, 2]:
                for rings in list(combinations(r, ring_count)):
                    cost = curr_w[0] + curr_a[0]
                    cost += sum(ring[0] for ring  in rings)
                    p = (100,curr_w[1] +sum(ring[1] for ring  in rings) , curr_a[2] +sum(ring[2] for ring  in rings))

                    if battle(p,b) and cost < min_cost:
                        min_cost = cost

    print(min_cost)



@profiler
def part2():

    with open('input.txt') as f:
        w, a, r = f.read().split('\n\n')

    w, a, r = w.split('\n')[1:], a.split('\n')[1:], r.split('\n')[1:]

    w = [(int(i.split()[1]), int(i.split()[2]), int(i.split()[3])) for i in w]
    a = [(int(i.split()[1]), int(i.split()[2]), int(i.split()[3])) for i in a]
    r = [(int(i.split()[2]), int(i.split()[3]), int(i.split()[4])) for i in r]

    a.append((0, 0, 0))  # no armor choice

    b = (100, 8, 2)  # input

    max_cost = 0
    for curr_w in w:
        for curr_a in a:
            for ring_count in [0, 1, 2]:
                for rings in list(combinations(r, ring_count)):
                    cost = curr_w[0] + curr_a[0]
                    cost += sum(ring[0] for ring  in rings)
                    p = (100,curr_w[1] +sum(ring[1] for ring  in rings) , curr_a[2] +sum(ring[2] for ring  in rings))

                    if not battle(p,b) and cost > max_cost:
                        max_cost = cost

    print(max_cost)


if __name__ == "__main__":

    part1()
    part2()
