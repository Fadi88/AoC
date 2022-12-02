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
        g = l.split()
        freq[l.strip()] += 1

    score = 0
    wins = {(0, 1), (1, 2), (2, 0)}
    for g in freq:
        hands = g.split()

        g_score = ord(hands[1]) - ord('X') + 1
        if ord(hands[0]) - ord('A') == ord(hands[1]) - ord('X'):
            g_score += 3
        elif (ord(hands[0]) - ord('A'), ord(hands[1]) - ord('X')) in wins:
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

    val = {
        'A': {'X': 3, 'Y': 1 + 3, 'Z': 2 + 6},
        'B': {'X': 1, 'Y': 2 + 3, 'Z': 3 + 6},
        'C': {'X': 2, 'Y': 3 + 3, 'Z': 1 + 6},
    }
    for g in freq:
        hands = g.split()
        score += val[hands[0]][hands[1]] * freq[g]

    print(score)


if __name__ == "__main__":

    part1()
    part2()
