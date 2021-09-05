import time,os,re

def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        method(*arg, **kw)
        print('Method '  + method.__name__ +' took : ' + "{:2.5f}".format(time.time()-t) + ' sec')
    return wrapper_method


def is_nice(l):
    has_vowels = len(re.findall(r'[aeiou]', l)) > 2
    has_repeated = any([l[i] == l[i+1] for i in range(len(l)-1)])
    has_bad = 'ab' in l or 'cd' in l or 'pq' in l or 'xy' in l
    return has_vowels and has_repeated and not has_bad

def is_nice_2(l):
    has_repeated = re.match(r'.*(\w\w).*\1.*' , l) is not None
    has_chars = re.match(r'.*(\w)\w\1.*' , l) is not None
    return has_repeated and has_chars

@profiler
def part1():
    with open('input.txt', 'r') as f:
        print(sum([*map(is_nice,f.read().split('\n'))]))
            

@profiler
def part2():
    with open('input.txt', 'r') as f:
        print(sum([*map(is_nice_2,f.read().split('\n'))]))


if __name__ == "__main__":

    part1()
    part2()
