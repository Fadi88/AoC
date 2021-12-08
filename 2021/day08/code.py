import time


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
    # 2 : 1
    # 3 : 7
    # 4 : 4,
    # 5 : 2,3,5,
    # 6 : 0,6,9
    # 7 : 8

    cnt = 0
    for l in open("day08/input.txt"):
        l = l.split(' | ')
        patterns = l[1].split()
        for pattern in patterns:
            if len(pattern) in [2, 4, 3, 7]:
                cnt += 1

    print("part 1 : ", cnt)


@profiler
def part2():
    seg = set(['a', 'b', 'c', 'd', 'e', 'f', 'g'])

    # 2 : 1
    # 3 : 7
    # 4 : 4,
    # 5 : 2,3,5
    # 6 : 0,6,9
    # 7 : 8

    total = 0

    for l in open("day08/input.txt"):
        #mapping = {i: seg for i in range(10)}
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
            if len(pattern) == 6:  # 0,6,9
                if len(mapping[1] - set(pattern)) == 1:  # 6
                    mapping[6] = set(pattern)

        for pattern in patterns:
            if len(pattern) == 5:  # 2,3,5
                if len(mapping[1] - set(pattern)) == 0:  # 3
                    mapping[3] = set(pattern)
                elif len(set(pattern) - mapping[6]) == 0:  # 5
                    mapping[5] = set(pattern)
                elif len(set(pattern) - mapping[6]) == 1:  # 2
                    mapping[2] = set(pattern)

        for pattern in patterns:
            if len(pattern) == 6 and set(pattern) not in mapping:  # 0,9
                if len(mapping[5] - set(pattern)) == 0:
                    mapping[9] = set(pattern)
                else:
                    mapping[0] = set(pattern)

        s = ""
        for p in l[1].split(" "):
            s += str(mapping.index(set(p.strip())))
        
        total += int(s)

    print(total)
            

if __name__ == "__main__":

    part1()
    part2()
