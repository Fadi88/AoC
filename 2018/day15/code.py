# pylint: disable=C0114,C0116,C0301,C0209,W1514,C0414,E0001,R0914

from typing import Any
import os
from time import perf_counter_ns
from collections import deque

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


class Unit:
    def __init__(self, pos, Team):
        self.pos = pos
        self.team = Team
        self.hp = 200
        self.attack = 3

    def is_alive(self):
        return self.hp > 0

    def __eq__(self, other):
        if isinstance(other, tuple):
            return self.pos == other
        return False

    def __hash__(self):
        return hash(self.pos)

    def __repr__(self):
        return f"Unit({self.pos}, {self.team}, {self.hp}, {self.attack})"


def is_next_to(u, units):
    enemy_units = [ou for ou in units if u.team != ou.team and ou.is_alive()]
    n = []
    for dx, dy in [(0, -1), (-1, 0), (1, 0), (0, 1)]:
        if (u.pos[0]+dx, u.pos[1]+dy) in enemy_units:
            for e in enemy_units:
                if e.pos == (u.pos[0]+dx, u.pos[1]+dy):
                    n.append(e)
    return n


def get_adjacent_positions(pos):
    x, y = pos
    return [(x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)]


def reading_order(pos):
    return pos[1], pos[0]


def find_target_position(unit, units, free_space):
    alive_units = [ou for ou in units if ou.is_alive()]
    enemy_positions = {
        enemy.pos for enemy in alive_units if enemy.team != unit.team}
    in_range_positions = {
        adj for pos in enemy_positions for adj in get_adjacent_positions(pos) if adj in free_space
    }

    queue = deque([(unit.pos, None, 0)])
    visited = set()

    possible = {}
    while queue:
        current, first_step, d = queue.popleft()
        if current in visited:
            continue
        visited.add(current)

        if current in in_range_positions:
            if current not in possible:
                possible[current] = (d, first_step)
        for neighbor in get_adjacent_positions(current):
            if neighbor in free_space and neighbor not in visited and neighbor not in alive_units:
                queue.append((neighbor, first_step or neighbor, d+1))

    if possible:
        min_val = min(v[0] for v in possible.values())
        ret = [v[1] for v in possible.values() if v[0] == min_val]
        ret.sort(key=reading_order)
        if len(set(ret)) > 1:
            target_vals = {(min_val, r) for r in ret}
            targets = [k for k, v in possible.items() if v in target_vals]
            targets.sort(key=reading_order)
            return possible[targets[0]][1]
        return ret[0]
    return None


def battle(units, free_space):
    round = 0
    while True:
        units = [u for u in units if u.is_alive()]
        units = sorted(units, key=lambda u: (u.pos[1], u.pos[0]))

        for u in units:
            if not u.is_alive():
                continue
            if not is_next_to(u, units):
                new_pos = find_target_position(u, units, free_space)
                if new_pos:
                    u.pos = new_pos
            if e := is_next_to(u, units):
                e.sort(key=lambda u: u.hp)
                e[0].hp -= u.attack
                if all(not u.is_alive() for u in units if u.team == "E") or all(not u.is_alive() for u in units if u.team == "G"):
                    return round, units

        # print(round, sum(u.hp for u in units if u.Team == "G"))
        round += 1


@profiler
def part_1():
    free_space, units = set(), set()

    with open(input_file) as f:
        for y, l in enumerate(f.read().splitlines()):
            for x, c in enumerate(l):
                if c in "GE":
                    units.add(Unit((x, y), c))
                if c in "GE.":
                    free_space.add((x, y))

    round, units = battle(units, free_space)
    print(round * sum(u.hp for u in units if u.is_alive()))


@ profiler
def part_2():
    free_space, units = set(), set()

    with open(input_file) as f:
        for y, l in enumerate(f.read().splitlines()):
            for x, c in enumerate(l):
                if c in "GE":
                    units.add(Unit((x, y), c))
                if c in "GE.":
                    free_space.add((x, y))

    low = 0
    high = 100
    elf_cnt = sum(u.team == "E" for u in units)
    while low < high:
        mid = (low + high) // 2
        units_copy = []
        for u in units:
            if u.team == "E":
                units_copy.append(Unit(u.pos, u.team))
                units_copy[-1].attack += mid
            else:
                units_copy.append(Unit(u.pos, u.team))

        _, units_res = battle(units_copy, free_space)

        if sum(u.team == "E" for u in units_res) == elf_cnt:
            high = mid
        else:
            low = mid + 1

    units_copy = []
    for u in units:
        if u.team == "E":
            units_copy.append(Unit(u.pos, u.team))
            units_copy[-1].attack += high
        else:
            units_copy.append(Unit(u.pos, u.team))

    round, units = battle(units_copy, free_space)
    print(round * sum(u.hp for u in units if u.is_alive()))


if __name__ == "__main__":
    part_1()
    part_2()
