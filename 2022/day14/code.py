from time import perf_counter


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print('Method ' + method.__name__ + ' took : ' +
              "{:2.5f}".format(perf_counter()-t) + ' sec')
        return ret
    return wrapper_method


def move_down(pos):
    return (pos[0], pos[1] + 1)


def move_diag_left(pos):
    return (pos[0] - 1, pos[1] + 1)


def move_diag_right(pos):
    return (pos[0] + 1, pos[1] + 1)


@profiler
def part1():
    particles = {}
    for l in open("input.txt"):
        p = [*map(lambda x: tuple(map(int, (x.split(",")))),  l.split(" -> "))]

        for i in range(1, len(p)):
            p1, p2 = p[i-1], p[i]

            if p1[0] == p2[0]:
                for y in range(min([p1[1], p2[1]]), max([p1[1], p2[1]]) + 1):
                    particles[(p1[0], y)] = '#'
            elif p1[1] == p2[1]:
                for x in range(min([p1[0], p2[0]]), max([p1[0], p2[0]]) + 1):
                    particles[(x, p1[1])] = '#'
            else:
                assert(False)

    source = (500, 0)

    max_y = max(set(map(lambda x: x[1], particles)))

    fallen_sand = 0

    while True:  # a new sand particle falls
        pos = (source[0], source[1])
        fallen_sand += 1
        while True:  # the same particle keep falling
            if move_down(pos) not in particles:
                pos = move_down(pos)
            elif move_diag_left(pos) not in particles:
                pos = move_diag_left(pos)
            elif move_diag_right(pos) not in particles:
                pos = move_diag_right(pos)
            else:  # cant fall anymore
                particles[pos] = '0'
                break

            if pos[1] > max_y:
                print(fallen_sand - 1)
                return


@profiler
def part2():
    particles = {}
    for l in open("input.txt"):
        p = [*map(lambda x: tuple(map(int, (x.split(",")))),  l.split(" -> "))]

        for i in range(1, len(p)):
            p1, p2 = p[i-1], p[i]

            if p1[0] == p2[0]:
                for y in range(min([p1[1], p2[1]]), max([p1[1], p2[1]]) + 1):
                    particles[(p1[0], y)] = '#'
            elif p1[1] == p2[1]:
                for x in range(min([p1[0], p2[0]]), max([p1[0], p2[0]]) + 1):
                    particles[(x, p1[1])] = '#'
            else:
                assert(False)

    source = (500, 0)

    max_y = max(set(map(lambda x: x[1], particles)))

    fallen_sand = 0

    while True:  # a new sand particle falls
        pos = (source[0], source[1])
        fallen_sand += 1
        while True:  # the same particle keep falling
            if move_down(pos) not in particles:
                pos = move_down(pos)
            elif move_diag_left(pos) not in particles:
                pos = move_diag_left(pos)
            elif move_diag_right(pos) not in particles:
                pos = move_diag_right(pos)
            else:  # cant fall anymore
                if pos == source:
                    print(fallen_sand)
                    return
                particles[pos] = '0'
                break
            if pos[1] == 1 + max_y:
                particles[pos] = '0'
                break


if __name__ == "__main__":

    part1()
    part2()
