import time,os

def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        method(*arg, **kw)
        print('Method '  + method.__name__ +' took : ' + "{:2.5f}".format(time.time()-t) + ' sec')
    return wrapper_method

@profiler
def part1():
  
    pos = 0 + 0j
    dr = 0 + 1j

    with open('input.txt', 'r') as f_in :
        ls = f_in.read().strip().split(', ')

    for m in ls:
        if 'R' in m:
            dr *= -1j
        else :
            dr *= 1j

        pos += dr*int(m[1:])

    print(abs(pos.real) + abs(pos.imag))

@profiler
def part2():

    visited = set()
    pos = 0 + 0j
    dr = 0 + 1j

    with open('input.txt', 'r') as f_in :
        ls = f_in.read().strip().split(', ')

    for m in ls:
        if 'R' in m:
            dr *= -1j
        else :
            dr *= +1j

        for _ in range(int(m[1:])):
            pos += dr

            if pos not in visited:
                visited.add(pos)
            else :
                print(abs(pos.real) + abs(pos.imag))
                return

if __name__ == "__main__":

    part1()
    part2()
