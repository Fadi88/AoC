import time
import re
import hashlib


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

    Traps = []
    Traps.append([c == '^' for c in open('input.txt').read().strip()])
    #Traps.append([c == '^' for c in '.^^.^.^^^^'])
    # Traps.append([False,False,True,True,False])

    for l in range(1, 40):
        Traps.append([])
        for x in range(len(Traps[0])):
            center = Traps[l-1][x]
            if 0 < x < len(Traps[0]) - 1:
                left = Traps[l-1][x-1]
                right = Traps[l-1][x+1]
            elif x == 0:
                left = False
                right = Traps[l-1][x+1]
            elif x == len(Traps[0]) - 1:
                left = Traps[l-1][x-1]
                right = False

            if left == center == True and right == False:
                Traps[l].append(True)
            elif center == right == True and left == False:
                Traps[l].append(True)
            elif left == True and center == right == False:
                Traps[l].append(True)
            elif right == True and center == left == False:
                Traps[l].append(True)
            else:
                Traps[l].append(False)

    print(len(Traps)*len(Traps[0]) - sum(map(sum, Traps)))


@profiler
def part2():

    Traps = []
    Traps.append([c == '^' for c in open('input.txt').read().strip()])

    for l in range(1, 400000):
        Traps.append([])
        for x in range(len(Traps[0])):
            center = Traps[l-1][x]
            if 0 < x < len(Traps[0]) - 1:
                left = Traps[l-1][x-1]
                right = Traps[l-1][x+1]
            elif x == 0:
                left = False
                right = Traps[l-1][x+1]
            elif x == len(Traps[0]) - 1:
                left = Traps[l-1][x-1]
                right = False

            if left == center == True and right == False:
                Traps[l].append(True)
            elif center == right == True and left == False:
                Traps[l].append(True)
            elif left == True and center == right == False:
                Traps[l].append(True)
            elif right == True and center == left == False:
                Traps[l].append(True)
            else:
                Traps[l].append(False)

    print(len(Traps)*len(Traps[0]) - sum(map(sum, Traps)))


if __name__ == "__main__":

    part1()
    part2()
