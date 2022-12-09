from time import perf_counter

def profiler(method):
    def wrapper_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print('Method ' + method.__name__ + ' took : ' +
              "{:2.5f}".format(perf_counter()-t) + ' sec')
        return ret
    return wrapper_method


def follow(head, tail):
    dx = head[0] - tail[0]
    dy = head[1] - tail[1]

    if (abs(dx) > 1 and dy == 0) or (abs(dy) > 1 and dx == 0):  # straight line move
        return (tail[0] + dx//2, tail[1] + dy//2)
    elif abs(dx) > 1 or abs(dy) > 1:  # diagonal move
        around_head = set([(head[0] + nx, head[1] + ny) for nx in (0, 1, -1)
                          for ny in (0, 1, -1) if not nx == ny == 0])
        around_tail = set([(tail[0] + nx, tail[1] + ny)
                          for nx in (1, -1) for ny in (1, -1)])
        return around_head.intersection(around_tail).pop()
    else:
        return tail


@profiler
def part1():
    head = (0, 0)
    tail = (0, 0)

    vis = set()
    deltas = {"R": (1, 0), "L": (-1, 0), "U": (0, 1), "D": (0, -1)}

    for l in open("input.txt").read().splitlines():

        delta = deltas[l.split()[0]]

        for _ in range(int(l.split()[1])):
            head = (head[0] + delta[0], head[1] + delta[1])

            tail = follow(head, tail)
    
            vis.add(tail)

    print(len(vis))


@profiler
def part2():
    rope = [(0, 0)for _ in range(10)]
    vis = set()

    deltas = {"R": (1, 0), "L": (-1, 0), "U": (0, 1), "D": (0, -1)}

    for l in open("input.txt").read().splitlines():

        delta = deltas[l.split()[0]]

        for _ in range(int(l.split()[1])):
            rope[0] = (rope[0][0] + delta[0], rope[0][1] + delta[1])

            for i in range(1, len(rope)):
                rope[i] = follow(rope[i-1], rope[i])

            vis.add(rope[-1])

    print(len(vis))


if __name__ == "__main__":

    part1()
    part2()
