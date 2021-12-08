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
    cnt = 0
    for l in open("day08/input.txt"):
        patterns = l.split(' | ')[1].split()

        cnt += sum([len(pattern) in [2, 4, 3, 7] for pattern in patterns])

    print("part 1 : ", cnt)


@profiler
def part2():
    seg = set(['a', 'b', 'c', 'd', 'e', 'f', 'g'])

    total = 0

    for l in open("day08/input.txt"):
        mapping = [set()] * 10

        l = l.split(' | ')
        patterns = l[0].split(" ")
        for pattern in patterns:
            if len(pattern) == 2:  # 1
                mapping[1] = set(pattern)
            elif len(pattern) == 4:  # 4
                mapping[4] = set(pattern)
            elif len(pattern) == 3:  # 7
                mapping[7] = set(pattern)
            elif len(pattern) == 7:  # 8
                mapping[8] = set(pattern)

        for pattern in patterns:
            if len(pattern) == 5:  # 2,3,5
                if len(mapping[1] - set(pattern)) == 0:  # 3
                    mapping[3] = set(pattern)
                elif len(set(pattern) - mapping[4]) == 2:  # 5
                    mapping[5] = set(pattern)
                elif len(set(pattern) - mapping[4]) == 3:  # 2
                    mapping[2] = set(pattern)

        for pattern in patterns:
            if len(pattern) == 6:  # 0,6,9
                if len(mapping[1] - set(pattern)) == 1:  # 6
                    mapping[6] = set(pattern)
                elif len(mapping[5] - set(pattern)) == 0:
                    mapping[9] = set(pattern)
                else:
                    mapping[0] = set(pattern)

        s = ""
        for p in l[1].split(" "):
            s += str(mapping.index(set(p.strip())))

        total += int(s)

    print("part 2 : ", total)


@profiler
def part2_segment():
    t = ['abcefg', 'cf', 'acdeg', 'acdfg', 'bcdf', 'abdfg', 'abdefg',
         'acf', 'abcdefg', 'abcdfg']

    ref = defaultdict(list)

    for i in set(''.join(t)):
        ref[''.join(t).count(i)].append(i)

    total = 0
    for l in open('day08/input.txt'):

        p = l.strip().split(' | ')

        freq = {}

        for i in set(''.join(p[0].split(' '))):
            freq[i] = ''.join(p[0]).count(i)

        mapping = {}

        four = list(filter(lambda x: len(x) == 4, p[0].split(' ')))[0]
        for i in freq:
            if freq[i] in [4, 6, 9]:
                mapping[i] = ref[freq[i]][0]
            elif freq[i] == 7:
                mapping[i] = 'd' if i in four else 'g'
            elif freq[i] == 8:
                mapping[i] = 'c' if i in four else 'a'

        val = ''
        for pat in p[1].split(' '):
            v = ''.join(sorted([mapping[ch] for ch in pat]))

            val += str(t.index(v))

        total += int(val)

    print(total)


if __name__ == "__main__":

    part1()
    part2()
    part2_segment()
