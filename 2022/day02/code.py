import time

from collections import Counter, defaultdict


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
    freq = Counter(open("input.txt").read().splitlines())

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
    freq = Counter(open("input.txt").read().splitlines())

    score = 0
    for g in freq:
        hands = g.split()

        second_hand_shift = ord(hands[1]) - ord('X')

        g_score = second_hand_shift * 3 + \
            (ord(hands[0]) - ord('A') + second_hand_shift - 1) % 3 + 1

        score += g_score * freq[g]

    print(score)


if __name__ == "__main__":

    part1()
    part2()
