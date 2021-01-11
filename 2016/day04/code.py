import time
import os
from collections import Counter


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        method(*arg, **kw)
        print('Method ' + method.__name__ + ' took : ' +
              "{:2.5f}".format(time.time()-t) + ' sec')
    return wrapper_method


@profiler
def part1():

    with open('input.txt') as f_in:

        cnt = 0
        for l in f_in.read().split('\n'):
            checksum = l[l.find('[')+1:-1]
            p = l[:l.find('[')].split('-')
            sec_id = int(p[-1])
            name = ''.join(p[:-1])
            freq = list(Counter(name).values())
            freq.sort(reverse=True)
            freq = freq[:5]

            if sum([True for idx, c in enumerate(checksum) if name.count(c) == freq[idx]]) == len(checksum):
                cnt += sec_id

        print(cnt)


@profiler
def part2():

    with open('input.txt') as f_in:

        for l in f_in.read().split('\n'):
            checksum = l[l.find('[')+1:-1]
            p = l[:l.find('[')].split('-')
            sec_id = int(p[-1])
            name = ''.join(p[:-1])
            freq = list(Counter(name).values())
            freq.sort(reverse=True)
            freq = freq[:5]

            if sum([True for idx, c in enumerate(checksum) if name.count(c) == freq[idx]]) == len(checksum):
                name = ' '.join(p[:-1])
                dec = ''
                for c in name:
                    if c == ' ':
                        dec += ' '
                    else:
                        new_c =  (ord(c)-ord('a')+(sec_id % 26))%26
                        dec += chr(ord('a') + new_c)
                if 'north' in dec:
                    print(sec_id)
                    break


if __name__ == "__main__":

    part1()
    part2()
