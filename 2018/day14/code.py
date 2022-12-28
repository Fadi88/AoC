from collections import Counter
import time


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print("Method " + method.__name__ + " took : " +
              "{:2.5f}".format(time.time() - t) + " sec")
        return ret

    return wrapper_method


@profiler
def part_1():
    input = 652601
    score = [3, 7]

    e1 = 0
    e2 = 1

    while len(score) - 10 < input:
        s = score[e1] + score[e2]
        score.extend([int(i) for i in str(s)])

        e1 = (e1 + 1 + score[e1]) % len(score)
        e2 = (e2 + 1 + score[e2]) % len(score)

    print("".join(str(s) for s in score[input:input+10]))


@profiler
def part_2():
    input = 652601
    score = [3, 7]

    e1 = 0
    e2 = 1

    while str(input) not in "".join(str(x) for x in score[-(len(str(input)) + 1):]):
        s = score[e1] + score[e2]
        score.extend([int(i) for i in str(s)])

        e1 = (e1 + 1 + score[e1]) % len(score)
        e2 = (e2 + 1 + score[e2]) % len(score)

    l = "".join(str(x) for x in score[-(len(str(input)) + 1):]).replace(str(input) , "")
    

    print(len(score) - len(str(input)) - len(l))


if __name__ == "__main__":

    part_1()
    part_2()
