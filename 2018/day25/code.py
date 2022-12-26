from collections import defaultdict, deque
import time


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print("Method " + method.__name__ + " took : " +
              "{:2.5f}".format(time.time() - t) + " sec")
        return ret

    return wrapper_method


def get_dst(p1, p2):
    return sum(abs(p1[i] - p2[i]) for i in range(4))


@profiler
def part_1():
    pts = [tuple(map(int, l.split(",")))
           for l in open("input.txt").read().splitlines()]

    grid = defaultdict(set)

    for p1 in pts:
        for p2 in pts:
            if p1 == p2:
                continue
            if get_dst(p1,p2) <= 3:
                grid[p1].add(p2)

    visited = defaultdict(bool)
    cc = 0

    for p in pts:
        if visited[p] == False:

            to_visit = deque()
            to_visit.append(p)

            while to_visit:
                current_pt = to_visit.popleft()

                visited[current_pt] = True

                for np in grid[current_pt]:
                    if visited[np] == False:
                        to_visit.append(np)

            cc += 1

    print(cc)


if __name__ == "__main__":

    part_1()
