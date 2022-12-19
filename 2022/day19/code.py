from time import time as perf_counter
from collections import deque, defaultdict
from copy import deepcopy
import re


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print('Method ' + method.__name__ + ' took : ' +
              "{:2.5f}".format(perf_counter()-t) + ' sec')
        return ret
    return wrapper_method


class state:
    def __init__(self):
        self.time = 0
        self.ore_bot = 1
        self.ore = 0
        self.clay_bot = 0
        self.clay = 0
        self.obsidian_bot = 0
        self.obsidian = 0
        self.geode_bot = 0
        self.geode = 0

    def __str__(self):
        ret = str(self.time) + " "
        ret += "or " + str(self.ore) + "  bot " + str(self.ore_bot) + "  "
        ret += "cl " + str(self.clay) + "  bot " + str(self.clay_bot) + "  "
        ret += "ob " + str(self.obsidian) + "  " + \
            str(self.obsidian_bot) + "  "
        ret += "ge " + str(self.geode) + " bot " + str(self.geode_bot)

        return ret

def get_max_geode(blue_print, limit=24):

    init_state = state()

    possible_scores = []

    to_visit = deque()
    to_visit.append(init_state)

    seen = set()

    best_geode = defaultdict(int)

    global cycles

    while to_visit:
        current_state = to_visit.popleft()

        if str(current_state) in seen:
            continue

        seen.add(str(current_state))

        current_state.time += 1

        if current_state.time > limit:
            possible_scores.append(blue_print[0] * current_state.geode)
            continue

        n_cl, n_or, n_ob, n_ge = (0, 0, 0, 0)

        if current_state.ore >= blue_print[1]:
            n_or = 1

        if current_state.ore >= blue_print[2]:
            n_cl = 1

        if current_state.ore >= blue_print[3] and current_state.clay >= blue_print[4]:
            n_ob = 1

        if current_state.ore >= blue_print[5] and current_state.obsidian >= blue_print[6]:
            n_ge = 1

        current_state.ore += current_state.ore_bot
        current_state.clay += current_state.clay_bot
        current_state.geode += current_state.geode_bot
        current_state.obsidian += current_state.obsidian_bot

        # hack 1 dont explore paths with less geode than previously found at the same time step
        delta = 1 if limit != 24 and current_state.time in [
            22, 23, 24, 25, 26] else 0
        if current_state.geode + delta < best_geode[current_state.time]:
            continue
        elif current_state.geode > best_geode[current_state.time]:
            best_geode[current_state.time] = current_state.geode

        # hack 2 always favor geode bots and dont explore other options
        if n_ge == 1:
            new_state = deepcopy(current_state)
            new_state.geode_bot += 1
            new_state.ore -= blue_print[5]
            new_state.obsidian -= blue_print[6]

            assert(new_state.ore >= 0 and new_state.obsidian >= 0)

            to_visit.append(new_state)
            continue

        # hack 3 dont create more bots than what makes you able to build any robot in once cycle
        if n_ob == 1 and current_state.obsidian_bot < blue_print[6]:
            new_state = deepcopy(current_state)
            new_state.obsidian_bot += 1
            new_state.ore -= blue_print[3]
            new_state.clay -= blue_print[4]

            assert(new_state.ore >= 0 and new_state.clay >= 0)

            to_visit.append(new_state)

        if n_cl == 1 and current_state.clay_bot < blue_print[4]:
            new_state = deepcopy(current_state)
            new_state.clay_bot += 1
            new_state.ore -= blue_print[2]

            assert(new_state.ore >= 0)

            to_visit.append(new_state)

        if n_or == 1 and current_state.ore_bot < max([blue_print[1], blue_print[2], blue_print[3], blue_print[5]]):
            new_state = deepcopy(current_state)
            new_state.ore_bot += 1
            new_state.ore -= blue_print[1]

            assert(new_state.ore >= 0)

            to_visit.append(new_state)

        to_visit.append(current_state)

    return max(possible_scores)


@profiler
def part1():
    blue_prints = []

    for l in open("input.txt").read().splitlines():
        blue_prints.append(list(map(int, re.findall(r"\d+", l))))

    print(sum(get_max_geode(blue_print, 24) for blue_print in blue_prints))


@profiler
def part2():
    blue_prints = []

    for l in open("input.txt").read().splitlines():
        blue_prints.append(list(map(int, re.findall(r"\d+", l))))

    l = list(get_max_geode(blue_print, 32) for blue_print in blue_prints[:3])

    prod = 1
    for i in range(3):
        prod *= l[i] // blue_prints[i][0]

    print(prod)


if __name__ == "__main__":

    part1()
    part2()
