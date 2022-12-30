import time
from collections import defaultdict, deque


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print("Method " + method.__name__ + " took : " +
              "{:2.5f}".format(time.time() - t) + " sec")
        return ret

    return wrapper_method


@profiler
def part1():
    comps = [(int(l.split("/")[0]), int(l.split("/")[1]))
             for l in open("day24/input.txt").read().splitlines()]

    to_visit = deque()

    for c in comps:
        if 0 in c:
            to_visit.append([c])

    strength = 0

    while to_visit:
        current_bridge = to_visit.popleft()

        for c in comps:
            if c in current_bridge:
                continue

            if len(current_bridge) == 1:
                val = current_bridge[-1][0] if current_bridge[-1][0] != 0 else current_bridge[-1][1]
                if val in c:
                    new_path = [] + current_bridge + [c]
                    to_visit.append(new_path)

            else:
                val = current_bridge[-1][0] if current_bridge[-1][0] not in current_bridge[-2] else current_bridge[-1][1]
                if val in c:
                    new_path = [] + current_bridge + [c]
                    to_visit.append(new_path)

        strength = max([strength, sum(c[0] + c[1]
                        for c in current_bridge)])

    print(strength)


@profiler
def part2():

    comps = [(int(l.split("/")[0]), int(l.split("/")[1]))
             for l in open("day24/input.txt").read().splitlines()]

    to_visit = deque()

    for c in comps:
        if 0 in c:
            to_visit.append([c])

    strength = defaultdict(set)

    while to_visit:
        current_bridge = to_visit.popleft()

        strength[len(current_bridge)].add(sum(c[0] + c[1]
                                              for c in current_bridge))

        for c in comps:
            if c in current_bridge:
                continue

            if len(current_bridge) == 1:
                val = current_bridge[-1][0] if current_bridge[-1][0] != 0 else current_bridge[-1][1]
                if val in c:
                    new_path = [] + current_bridge + [c]
                    to_visit.append(new_path)

            else:
                val = current_bridge[-1][0] if current_bridge[-1][0] not in current_bridge[-2] else current_bridge[-1][1]
                if val in c:
                    new_path = [] + current_bridge + [c]
                    to_visit.append(new_path)

    print(max(strength[max(strength.keys())]))


if __name__ == "__main__":

    part1()
    part2()
