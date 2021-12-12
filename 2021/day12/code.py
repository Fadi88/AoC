import time
from collections import defaultdict, deque


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
    grid = defaultdict(list)

    for l in open("day12/input.txt"):
        p = l.strip().split("-")
        if "start" in l:
            grid["start"].append(list(filter(lambda x: x != "start", p))[0])
        elif "end" in l:
            grid["end"].append(list(filter(lambda x: x != "end", p))[0])
        else:
            grid[p[1]].append(p[0])
            grid[p[0]].append(p[1])

    to_visit = deque()
    cnt = 0

    for i in grid["start"]:
        to_visit.append([i])

    while to_visit:
        current_path = to_visit.popleft()
        if current_path[-1] in grid["end"]:
            cnt += 1

        for i in grid[current_path[-1]]:
            tmp = current_path + [i]
            if i.islower() and i in current_path:
                continue
            else:
                to_visit.append(tmp)

    print(cnt)


def lower_pattern(tmp):
    lowers = [tmp.count(i) for i in set(tmp[1:]) if i.islower()]
    cnt = list(filter(lambda x: x > 2, lowers))
    return len(cnt) == 0 and lowers.count(2) < 2


@profiler
def part2():
    grid = defaultdict(list)

    for l in open("day12/input.txt"):
        p = l.strip().split("-")
        grid[p[1]].append(p[0])
        grid[p[0]].append(p[1])

    to_visit = deque()

    cnt = 0

    to_visit.append(["start"])

    while to_visit:
        current_path = to_visit.popleft()

        if current_path[-1] == "end":
            cnt += 1
            continue

        for i in grid[current_path[-1]]:
            if i == "start":
                continue
            tmp = current_path + [i]
            if not lower_pattern(tmp):
                continue
            else:
                to_visit.append(tmp)

    print(cnt)


if __name__ == "__main__":

    part1()
    part2()
