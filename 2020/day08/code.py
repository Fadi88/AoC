import time,os
from collections import defaultdict

class computer:
    def __init__(self):
        self.code = []
        self.acc  = 0
        self.pc   = 0
        self.term = False

    def set_code(self , in_code):
        self.code =in_code
        self.acc  = 0
        self.pc   = 0

    def exec(self):
        int_tracker = defaultdict(lambda : False)

        while self.pc != len(self.code) and not int_tracker[self.pc] == True:
            
            cur = self.code[self.pc]

            if cur[0] == 'nop':
                int_tracker[self.pc] = True
                self.pc += 1

            elif cur[0] == 'acc':
                int_tracker[self.pc] = True
                self.acc += cur[1]
                self.pc += 1

            elif cur[0] == 'jmp':
                int_tracker[self.pc] = True
                self.pc += cur[1]
            
            else :
                print('invalid inst')

        if self.pc == len(self.code):
            self.term = True


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        method(*arg, **kw)
        print('Method '  + method.__name__ +' took : ' + "{:2.5f}".format(time.time()-t) + ' sec')
    return wrapper_method

@profiler
def part1():

    inst = list()
    comp_obj = computer()
    for l in open('input.txt', 'r').readlines():
        tmp = l.strip().split()
        inst.append((tmp[0] , int(tmp[1])))

    comp_obj.set_code(inst)
    comp_obj.exec()
    print('part 1 answer : ' , comp_obj.acc)

@profiler
def part2():
    inst = list()
    comp_obj = computer()
    for l in open('input.txt', 'r').readlines():
        tmp = l.strip().split()
        inst.append((tmp[0] , int(tmp[1])))


    for l in range(len(inst)):
        if inst[l][0] == 'nop' or  inst[l][0] == 'jmp':
            mod = inst.copy()
            mod[l] = ['jmp' if inst[l][0] == 'nop' else 'nop' , inst[l][1]]
            comp_obj.set_code(mod)
            comp_obj.exec()

            if comp_obj.term == True:
                print('part 2 answer : ' , comp_obj.acc)
                break


if __name__ == "__main__":

    part1()
    part2()
