import time,os,re,math
from collections import defaultdict

def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print('Method '  + method.__name__ +' took : ' + "{:2.5f}".format(time.time()-t) + ' sec')
        return ret
    return wrapper_method

def matches(t1,t2):

    t1r = ''.join([t[-1] for t in t1])
    t2r = ''.join([t[-1] for t in t2])
    t1l = ''.join([t[0] for t in t1])
    t2l = ''.join([t[0] for t in t2])
    
    t1_edges = [t1[0] , t1[-1]  ,t1r , t1l]
    t2_edges = [t2[0] , t2[-1] , t2[0][::-1] , t2[-1][::-1] , t2l , t2l[::-1] ,t2r , t2r[::-1]]

    for et1 in t1_edges:
        for et2 in t2_edges:
            if et1 == et2:
                return True
    return False

def set_corner(cor , right , down):
    return cor

def remove_border(t):
    return t

def set_left_edge(t1,t2):
    ref = ''.join([t[-1] for t in t1])
    
    t2r = ''.join([t[-1] for t in t2])
    t2l = ''.join([t[0] for t in t2])

    if t2l == ref :
        pass
        # nothing to be done
    elif t2l[::-1] == ref :
        pass
        # flip hor
    elif t2r == ref :
        pass
        # flip ver
    elif t2r[::-1] == ref :
        pass
        # rotate 180
    elif t2[0] == ref :
        pass
        # mirror
    elif t2[0][::-1] == ref :
        pass
        # rotate 90 degree
    elif t2[-1] == ref :
        pass
        # rotate - 90 degree
    elif t2[-1][::-1] == ref :
        pass
        # rotate -90 and flip vertically

    return remove_border(t2)

def set_upper_edge(t1,t2):
    return remove_border(t2)

@profiler
def part1():
    tiles = defaultdict(list)
    for l in  open('input.txt'):
        if 'Tile' in l :
            tile = int(re.findall(r'\d+', l)[0])
        elif '.' in l or '#' in l:
            tiles[tile].append(l.strip())

    connected = defaultdict(set)

    for i in tiles :
        for t in tiles :
            if i == t : continue
            if matches(tiles[i],tiles[t]) :
                connected[i].add(t)
                connected[t].add(i)

    prod = 1

    for i in connected:
        if len(connected[i]) == 2:
            prod *= i
    print(prod)

@profiler
def part2():

    tiles = defaultdict(list)

    for l in  open('input.txt'):
        if 'Tile' in l :
            tile = int(re.findall(r'\d+', l)[0])
        elif '.' in l or '#' in l:
            tiles[tile].append(l.strip())

    connected = defaultdict(set)

    for i in tiles :
        for t in tiles :
            if i == t : continue
            if matches(tiles[i],tiles[t]) :
                connected[i].add(t)
                connected[t].add(i)

    sz = int(math.sqrt(len(connected)))
    image = [[0 for _ in range(sz)]for _ in range(sz)]
    for i in connected:
        if len(connected[i]) == 2:
            corner = i
            break

    image[0][0] = corner
    added = {corner}

    for y in range(1,sz):
        pos = connected[image[0][y-1]]
        for cand in pos :
            if cand not in added and len(connected[cand]) < 4:
                image[0][y] = cand
                added.add(cand)
                break
    
    for x in range(1,sz):
        for y in range(sz):
            pos = connected[image[x-1][y]]
            for cand in pos :
                if cand not in added:
                    image[x][y] = cand
                    added.add(cand)
                    break

    # set 0,0 tile
    tiles[image[0][0]] = set_corner(tiles[image[0][0]] , tiles[image[0][1]] , tiles[image[1][0]])

    for y,l in enumerate(image):
        print(l)
        if y != 0 :
            prv = image[y-1][0]
            tiles[l[0]] = set_upper_edge(tiles[prv] , tiles[l[0]])
        for x,tile in enumerate(l):
            if x != 0 :
                prv = image[y][x-1]
                tiles[tile] = set_left_edge(tiles[prv] , tiles[tile])

if __name__ == "__main__" :

    part1()
    part2()
