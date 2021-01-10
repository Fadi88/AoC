import random
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


def battle(actions, minimun_cost, hard_mode=0):
    cost = 0
    p_hp = 50
    p_mana = 500
    p_armor = 0

    b_hp = 55
    b_dam = 8

    active_attacks = defaultdict(int)

    for a in actions:
        p_hp -= hard_mode

        if p_hp == 0:
            break

        for atk in active_attacks:
            if atk == 'Shield':
                if active_attacks[atk] > 0:
                    active_attacks[atk] -= 1
                else:
                    p_armor -= 7
            elif atk == 'Poison':
                if active_attacks[atk] > 0:
                    b_hp -= 3
                    active_attacks[atk] -= 1
            elif atk == 'Recharge':
                if active_attacks[atk] > 0:
                    p_mana += 101
                    active_attacks[atk] -= 1

        if a == 'Magic Missile':
            p_mana -= 53
            cost += 53
            b_hp -= 4
        elif a == 'Drain':
            p_mana -= 73
            cost += 73
            p_hp += 2
            b_hp -= 2
        elif a == 'Shield':
            p_mana -= 113
            cost += 113
            p_armor += 7
            active_attacks['Shield'] += 5
        elif a == 'Poison':
            p_mana -= 173
            cost += 173
            active_attacks['Poison'] += 6
        elif a == 'Recharge':
            p_mana -= 229
            cost += 229
            active_attacks['Recharge'] += 5

        if p_mana < 1 or b_hp < 1:
            break

        if cost >= minimun_cost:
            return 0, 0, 0, 10

        for atk in active_attacks:
            if atk == 'Shield':
                if active_attacks[atk] > 0:
                    active_attacks[atk] -= 1
                else:
                    p_armor -= 7
            elif atk == 'Poison':
                if active_attacks[atk] > 0:
                    b_hp -= 3
                    active_attacks[atk] -= 1
            elif atk == 'Recharge':
                if active_attacks[atk] > 0:
                    p_mana += 101
                    active_attacks[atk] -= 1

        if b_hp < 1:
            break

        p_hp -= max(1, b_dam - p_armor)

        if p_hp < 1:
            break

    return cost, p_hp, p_mana, b_hp


@profiler
def part1():
    attacks = ['Magic Missile', 'Drain', 'Shield', 'Poison', 'Recharge']

    to_visit = [[a] for a in attacks]

    minimum_cost = 100000
    visited = []

    while to_visit:

        s = to_visit.pop(0)

        cost, p_hp, p_mana, b_hp = battle(s, minimum_cost)

        if p_hp > 0 and p_mana > 0 and b_hp > 0:
            for a in attacks:
                tmp = s.copy()
                tmp.append(a)
                tmp_cp = tmp.copy()
                if not tmp_cp in visited:
                    to_visit.append(tmp)
        elif b_hp < 1:
            if cost < minimum_cost:
                s.sort()
                visited.append(s)
                minimum_cost = cost

    print(minimum_cost)


@profiler
def part2():

    attacks = ['Magic Missile', 'Drain', 'Shield', 'Poison', 'Recharge']

    to_visit = [[a] for a in attacks]

    minimum_cost = 100000
    visited = []

    while to_visit:

        s = to_visit.pop(0)

        cost, p_hp, p_mana, b_hp = battle(s, minimum_cost, 1)

        if p_hp > 0 and p_mana > 0 and b_hp > 0:
            for a in attacks:
                tmp = s.copy()
                tmp.append(a)
                tmp_cp = tmp.copy()
                if not tmp_cp in visited:
                    to_visit.append(tmp)
        elif b_hp < 1:
            if cost < minimum_cost:
                s.sort()
                visited.append(s)

    print(minimum_cost)


if __name__ == "__main__":

    pass
    part1()
    part2()
