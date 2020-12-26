import time


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print('Method ' + method.__name__ + ' took : ' +
              "{:2.5f}".format(time.time()-t) + ' sec')
        return ret
    return wrapper_method


def manhaten_dist(p1, p2):
    return abs(p2[1]-p1[1]) + abs(p2[0]-p1[0])


@profiler
def part1():

    pts = [tuple(map(int, l.strip().split(',')))
           for l in open('input.txt', 'r')]
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    clusters_1 = {p: [p] for p in pts}

    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            min_dist = max_x * max_y
            chosen_p = None
            if (x, y) in pts:
                continue
            for p in pts:
                dst = manhaten_dist(p, (x, y))
                if dst < min_dist:
                    min_dist = dst
                    chosen_p = p
                elif dst == min_dist:
                    chosen_p = None

            if chosen_p is not None:
                clusters_1[chosen_p].append((x, y))

    clusters_2 = {p: [p] for p in pts}

    for x in range(min_x-1, max_x+2):
        for y in range(min_y-1, max_y+2):
            min_dist = max_x * max_y
            chosen_p = None
            if (x, y) in pts:
                continue
            for p in pts:
                dst = manhaten_dist(p, (x, y))
                if dst < min_dist:
                    min_dist = dst
                    chosen_p = p
                elif dst == min_dist:
                    chosen_p = None

            if chosen_p is not None:
                clusters_2[chosen_p].append((x, y))

    biggest = 0

    for ele in clusters_1:
        if len(clusters_1[ele]) > biggest and len(clusters_1[ele]) == len(clusters_2[ele]):
            biggest = len(clusters_1[ele])

    print(biggest)


@profiler
def part2():
    pts = [tuple(map(int, l.strip().split(',')))
           for l in open('input.txt', 'r')]
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    safe = set()
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            tmp = []
            for p in pts:
                tmp.append(manhaten_dist(p, (x, y)))

            if sum(tmp) < 10000:
                safe.add((x, y))

    print(len(safe))


if __name__ == "__main__":

    part1()
    part2()
