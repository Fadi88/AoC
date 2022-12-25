from time import time as perf_counter


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print('Method ' + method.__name__ + ' took : ' +
              "{:2.5f}".format(perf_counter()-t) + ' sec')
        return ret
    return wrapper_method


def get_decimal(snafu):
    ret = 0
    for idx, c in enumerate(snafu[::-1]):
        if c.isnumeric():
            ret += int(c) * 5**idx
        elif c == "-":
            ret += -1 * 5**idx
        elif c == "=":
            ret += -2 * 5**idx

    return ret


def get_snafu(n):

    ret = ""

    while n != 0:
        n, current_digit = divmod(n, 5)
        if current_digit in [0, 1, 2]:
            ret += str(current_digit)
        elif current_digit == 3:
            ret += "="
            n += 1
        elif current_digit == 4:
            ret += "-"
            n += 1

    return ret[::-1]


@profiler
def part1():
    print(get_snafu(sum(map(get_decimal, open("input.txt").read().splitlines()))))

if __name__ == "__main__":

    part1()
