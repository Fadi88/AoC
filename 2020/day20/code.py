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

def flip(t):
    ret = []
    for l in t:
        ret.append(l[::-1])
    return ret

def rotate(t):
    return [*map("".join, zip(*reversed(t)))]

def set_corner(cor , right , down):
    rr = ''.join([t[-1] for t in right])
    dr = ''.join([t[-1] for t in down])
    rl = ''.join([t[0] for t in right])
    dl = ''.join([t[0] for t in down])
    
    r_edges = [right[0] , right[-1] , right[0][::-1] , right[-1][::-1] , rr , rr[::-1] , rl , rl[::-1]]
    d_edges = [down[0] , down[-1] , down[0][::-1] , down[-1][::-1] , dr , dr[::-1] , dl , dl[::-1]]

    for _ in range(2):
        cor = flip(cor)
        for _ in range(4):
            cor = rotate(cor)
            if cor[-1] in d_edges and ''.join([t[-1] for t in cor]) in r_edges:
                return cor

    return None

def remove_border(t):
    return [x[1:-1] for x in t[1:-1]]

def set_left_edge(t1,t2):
    ref = ''.join([t[-1] for t in t1])

    for _ in range(2):
        t2 = flip(t2)
        for _ in range(4):
            t2 = rotate(t2)
            if ''.join([t[0] for t in t2]) == ref :
                return t2
    return None

def set_upper_edge(t1,t2):
    ref = t1[-1]
    for _ in range(2):
        t2 = flip(t2)
        for _ in range(4):
            t2 = rotate(t2)
            if t2[0] == ref :
                return t2
    return None

def assemble_image(img,tiles):
    whole_image = []

    for l in img:
        slice = [''] * len(tiles[l[0]])
        for t in l:
            for i,s in enumerate(tiles[t]):
                slice[i] += s
        for s in slice:
            whole_image.append(s)

    return whole_image

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

    tiles[image[0][0]] = set_corner(tiles[image[0][0]] , tiles[image[0][1]] , tiles[image[1][0]])

    for y,l in enumerate(image):
        if y != 0 :
            prv = image[y-1][0]
            tiles[l[0]] = set_upper_edge(tiles[prv] , tiles[l[0]])

        for x,tile in enumerate(l):
            if x != 0 :
                prv = image[y][x-1]
                tiles[tile] = set_left_edge(tiles[prv] , tiles[tile])

    for t in tiles:
        tiles[t] = remove_border(tiles[t])

    image = assemble_image(image,tiles)

    ky = 0
    monster = set()
    for l in open('monster.txt').read().split('\n'):
        kx = len(l)
        for i,ch in enumerate(l):
            if ch == '#':
                monster.add((i,ky))
        ky += 1

    for _ in range(2):
        image = flip(image)
        for _ in range(4):
            image = rotate(image)

            for x in range(0,len(image)-kx):
                for y in range(0,len(image)-ky):
                    parts = [] 
                    for i,p in enumerate(monster):
                        dx = x + p[0]
                        dy = y + p[1]
                        parts.append(image[dy][dx] == '#')
                    if all(parts) :
                        for p in monster:
                            dx = x + p[0]
                            dy = y + p[1]
                            image[dy] = image[dy][ : dx] + 'O' + image[dy][ dx +1 :]

    with open('output.txt' , 'w+') as f:
        for l in rotate(image):
            f.write(l + '\n' )

    print(sum([l.count('#') for l in image]))

if __name__ == "__main__" :

    part1()
    part2()