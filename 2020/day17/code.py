import time,os

def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print('Method '  + method.__name__ +' took : ' + "{:2.5f}".format(time.time()-t) + ' sec')
        return ret
    return wrapper_method

@profiler
def part1():
    l =  open('input.txt', 'r').read().split()
    map = [(x,y,0) for y,line in enumerate(l) for x,ch in enumerate(line) if ch == '#']

    for _ in range(6):
        act = {}
        new_map = []
        for x,y,z in map:
            for dx in [-1,0,1]:
                for dy in [-1,0,1]:
                    for dz in [-1,0,1]:
                        if dx == dy == dz == 0 : continue
                        elif (x+dx , y+dy , z+dz) in act: act[(x+dx , y+dy , z+dz)] += 1
                        else : act[(x+dx , y+dy , z+dz)] = 1

        for ele in act :
            if ele not in map and act[ele] == 3:
                new_map.append(ele)
            elif ele in map and act[ele] in [2,3]:
                new_map.append(ele)
 
        map = new_map
    print(len(map))
              

@profiler
def part2():

    l =  open('input.txt', 'r').read().split()
    map = [(x,y,0,0) for y,line in enumerate(l) for x,ch in enumerate(line) if ch == '#']

    for _ in range(6):
        act = {}
        new_map = []
        for x,y,z,w in map:
            for dx in [-1,0,1]:
                for dy in [-1,0,1]:
                    for dz in [-1,0,1]:
                        for dw in [-1,0,1]:
                            if dx == dy == dz == dw == 0  : continue
                            elif (x+dx , y+dy , z+dz , w+dw) in act: act[(x+dx , y+dy , z+dz , w+dw)] += 1
                            else : act[(x+dx , y+dy , z+dz , w+dw)] = 1

        for ele in act :
            if ele not in map and act[ele] == 3:
                new_map.append(ele)
            elif ele in map and act[ele] in [2,3]:
                new_map.append(ele)
 
        map = new_map
    print(len(map))

if __name__ == "__main__":
 
    part1()
    part2()
   