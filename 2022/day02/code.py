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

        h0 = ord(hands[0]) - ord('A')
        h1 = ord(hands[1]) - ord('X')

        # game score = value of hand(R1,P2,S3) + 3*(L0,T1,W2) 
        g_score = (h1 + 1) + 3 * ((h1 - h0 + 1) % 3)
        score += g_score * freq[g]

    print(score)


@profiler
def part2():
    freq = Counter(open("input.txt").read().splitlines())

    score = 0
    for g in freq:
        hands = g.split()

        h0 = ord(hands[0]) - ord('A')
        h1 = ord(hands[1]) - ord('X')

        g_score = h1 * 3 + (h0 + h1 - 1) % 3 + 1

        score += g_score * freq[g]

    print(score)


if __name__ == "__main__":

    part1()
    part2()
