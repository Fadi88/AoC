import time

from collections import defaultdict


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
    freq = defaultdict(int)
    for l in open("input.txt"):
        freq[l.strip()] += 1

    score = 0
    for g in freq:
        hands = g.split()

        g_score = ord(hands[1]) - ord('X') + 1

        if ord(hands[0]) - ord('A') == ord(hands[1]) - ord('X'):
            g_score += 3
        elif (ord(hands[0]) - ord('A') + 1) % 3 == ord(hands[1]) - ord('X'):
            g_score += 6

        score += g_score * freq[g]

    print(score)


@profiler
def part2():
    freq = defaultdict(int)
    for l in open("input.txt"):
        g = l.split()
        freq[l.strip()] += 1

    score = 0
    for g in freq:
        hands = g.split()

        g_score = 0
        if 'X' == hands[1]:  # loses
            g_score = 0 + (ord(hands[0]) - ord('A') - 1) % 3 + 1
        elif 'Y' == hands[1]:  # draw
            g_score = 3 + ord(hands[0]) - ord('A') + 1

        elif 'Z' == hands[1]:  # wins
            g_score = 6 + (ord(hands[0]) - ord('A') + 1) % 3 + 1

        score += g_score * freq[g]

    print(score)


if __name__ == "__main__":

    part1()
    part2()
