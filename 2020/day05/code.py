import time,os
import math

def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print('Method '  + method.__name__ +' took : ' + "{:2.5f}".format(time.time()-t) + ' sec')
        return ret
    return wrapper_method


@profiler
def part1():
    ids = []
    with open('input.txt', 'r') as f_in:
        for l in f_in:
            row_upp = 127
            row_low = 0
            col_upp = 7
            col_low = 0
            for dy in l[0:7]:
                if dy == 'F':
                    row_upp = int((row_upp + row_low) / 2.0)
                elif dy == 'B':
                    row_low = int(math.ceil((row_upp + row_low) / 2.0))

            for dx in l[7:10]:
                if dx == 'L':
                    col_upp = int((col_upp + col_low) / 2.0)
                elif dx == 'R':
                    col_low = int(math.ceil((col_upp + col_low) / 2.0))

            ids.append(row_low * 8 + col_low)
        print('part 1 answer : ' , max(ids))
    return ids


@profiler
def part2(ids):
    ids.sort()
    for i, idx in enumerate(ids):
        if  6 < idx < (127*8) and (idx - ids[i - 1]) == 2:
            print('part 2 answer : ' , idx - 1)
            break

if __name__ == "__main__":

    ids = part1()
    part2(ids)

    
    