# pylint: disable=C0114,C0116,C0301,C0209,W1514,C0414,E0001,R0914

from typing import Any
import os
from time import perf_counter_ns
import re

input_file = os.path.join(os.path.dirname(__file__), "input.txt")
# input_file = os.path.join(os.path.dirname(__file__), "test.txt")


def profiler(method):

    def wrapper_method(*args: Any, **kwargs: Any) -> Any:
        start_time = perf_counter_ns()
        ret = method(*args, **kwargs)
        stop_time = perf_counter_ns() - start_time
        time_len = min(9, ((len(str(stop_time))-1)//3)*3)
        time_conversion = {9: 'seconds', 6: 'milliseconds',
                           3: 'microseconds', 0: 'nanoseconds'}
        print(f"Method {method.__name__} took : {
              stop_time / (10**time_len)} {time_conversion[time_len]}")
        return ret

    return wrapper_method


class unit:
    def __init__(self, n, hp, init, dt, d, wk, im):
        self.num = n
        self.hp = hp
        self.init = init
        self.damage_type = dt
        self.damage = d
        self.weak = set(wk)
        self.immune = set(im)

    def get_power(self):
        return self.num * self.damage

    def calculate_damage(self, target):
        if self.damage_type in target.immune:
            return 0
        if self.damage_type in target.weak:
            return self.get_power() * 2
        return self.get_power()


def parse_unit(l):
    ps = tuple(map(int, re.findall(r"\d+", l)))
    cnt, hp, atk, init = ps

    damage_type = l.split()[-5]

    imm = re.findall(r"immune to .+?[\);]", l)
    imm = imm[0].replace("immune to ", "").replace(
        ";", "").replace(")", "").split(", ") if len(imm) > 0 else []

    wek = re.findall(r"weak to .+?[\);]", l)
    wek = wek[0].replace("weak to ", "").replace(
        ";", "").replace(")", "").split(", ") if len(wek) > 0 else []

    return unit(cnt, hp, init, damage_type, atk, wek, imm)


def select_targets(attackers, defenders):
    targets = {}
    attackers.sort(key=lambda u: (-u.get_power(), -u.init))
    for attacker in attackers:
        valid_targets = [
            d for d in defenders
            if d not in targets.values() and attacker.calculate_damage(d) > 0
        ]

        if valid_targets:
            valid_targets.sort(
                key=lambda d: (-attacker.calculate_damage(d), -d.get_power(), -d.init))
            targets[attacker] = valid_targets[0]
    return targets


def attack(attackers, targets):
    attackers.sort(key=lambda u: -u.init)
    for attacker in attackers:
        if attacker.num > 0 and attacker in targets:
            defender = targets[attacker]
            damage = attacker.calculate_damage(defender)
            killed = min(defender.num, damage // defender.hp)
            defender.num -= killed


def solve(immune, infect):
    previous_total_units = None

    while immune and infect:
        targets = {}
        targets.update(select_targets(immune, infect))
        targets.update(select_targets(infect, immune))

        attack(immune + infect, targets)
        current_total_units = sum(u.num for u in immune + infect)

        if current_total_units == previous_total_units:
            return 0, False

        previous_total_units = current_total_units

        immune = [u for u in immune if u.num > 0]
        infect = [u for u in infect if u.num > 0]

    return sum(u.num for u in immune + infect), bool(immune)


@profiler
def part_1():
    with open(input_file) as f:
        data = f.read().split("\n\n")

    imm = [parse_unit(l) for l in data[0].splitlines()[1:]]
    inf = [parse_unit(l) for l in data[1].splitlines()[1:]]

    print(solve(imm, inf)[0])


def solve_part_2(immune, infect):
    low = 1
    high = 10000
    while low < high:
        mid = (low + high) // 2
        immune_copy = [unit(u.num, u.hp, u.init, u.damage_type,
                            u.damage + mid, u.weak, u.immune) for u in immune]
        infect_copy = [unit(u.num, u.hp, u.init, u.damage_type,
                            u.damage, u.weak, u.immune) for u in infect]

        _, immune_wins = solve(immune_copy, infect_copy)

        if immune_wins:
            high = mid
        else:
            low = mid + 1

    immune_copy = [unit(u.num, u.hp, u.init, u.damage_type,
                        u.damage + high, u.weak, u.immune) for u in immune]
    infect_copy = [unit(u.num, u.hp, u.init, u.damage_type,
                        u.damage, u.weak, u.immune) for u in infect]
    return solve(immune_copy, infect_copy)


@ profiler
def part_2():
    with open(input_file) as f:
        data = f.read().split("\n\n")

    imm = [parse_unit(l) for l in data[0].splitlines()[1:]]
    inf = [parse_unit(l) for l in data[1].splitlines()[1:]]

    print(solve_part_2(imm, inf)[0])


if __name__ == "__main__":
    part_1()
    part_2()
