import time,os

def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        method(*arg, **kw)
        print('Method '  + method.__name__ +' took : ' + "{:2.5f}".format(time.time()-t) + ' sec')
    return wrapper_method

@profiler
def part1():

    with open('input.txt') as f_in :
        ls = [l for l in f_in.read().strip().split('\n')]

    pos = [1,1] 
    keypad = [[1,2,3] , [4,5,6] , [7,8,9]]

    for l in ls:
        for d in l:
            if d == 'U':
                pos[0] -= 1
                if pos[0] < 0 : pos[0] = 0

            elif d == 'D':
                pos[0] += 1
                if pos[0] == 3 : pos[0] = 2

            elif d == 'R':
                pos[1] += 1
                if pos[1] == 3 : pos[1] = 2

            elif d == 'L':
                pos[1] -= 1
                if pos[1] < 0 : pos[1] = 0

        print(keypad[pos[0]][pos[1]],end='')

    print()



@profiler
def part2():

    with open('input.txt') as f_in :
        ls = [l for l in f_in.read().strip().split('\n')]

    pos = [2,0] 
    keypad = [['0','0','1','0','0'], 
              ['0','2','3','4','0'], 
              ['5','6','7','8','9'],
              ['0','A','B','C','0'],
              ['0','0','B','0','0']
              ]

    for l in ls:
        for d in l:
            if d == 'U':
                new_pos = pos.copy()
                new_pos[0] = pos[0] - 1
                if new_pos[0] >= 0 and keypad[new_pos[0]][new_pos[1]] != '0':
                    pos = new_pos 
                
            elif d == 'D':
                new_pos = pos.copy()
                new_pos[0] = pos[0] + 1
                if new_pos[0] < 5 and keypad[new_pos[0]][new_pos[1]] != '0':
                    pos = new_pos 

            elif d == 'R':
                new_pos = pos.copy()
                new_pos[1] = pos[1] + 1
                if new_pos[1] < 5 and keypad[new_pos[0]][new_pos[1]] != '0':
                    pos = new_pos 

            elif d == 'L':
                new_pos = pos.copy()
                new_pos[1] = pos[1] - 1
                if new_pos[1] >= 0 and keypad[new_pos[0]][new_pos[1]] != '0':
                    pos = new_pos 

        print(keypad[pos[0]][pos[1]],end='')

    print()




if __name__ == "__main__":

    part1()
    part2()
