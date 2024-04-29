# pylint: disable=C0114,C0116,C0301,C0209,W1514

from time import perf_counter

def profiler(method):
    def wrapper_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print("Method " + method.__name__ + " took : " + "{:2.5f}".format(perf_counter() - t) + " sec")
        return ret

    return wrapper_method


@profiler
def part1():
    maze = [list(l.strip()) for l in open("day23/input.txt").readlines()]
    start = (maze[0].index(".") ,0)

    ly = len(maze)
    lx = len(maze[0])
    deltas = {
        "<" : (-1,0),
        ">" : (1,0),
        "v" : (0,1),
        "^" : (0,-1)
    }

    to_visit = [( frozenset(start),start)]

    pathes_len = []

    while to_visit:
        path,(px,py) = to_visit.pop()
        c = maze[py][px]
        
        for dx,dy in deltas.values() if not c in deltas else [deltas[c]]:
            nx , ny = px + dx , py + dy
            if ly > ny > 0 and lx > nx >0:
                nc = maze[ny][nx]

                if (nx,ny) in path:
                    continue
                
                if nc != "#":
                    n_path = set(path)
                    n_path.add((nx,ny))
                    to_visit.append((n_path,(nx,ny)))

                if ny == ly - 1:
                    pathes_len.append(len(path)-1)
    print(max(pathes_len)-1)

def explore_pt(maze,junctions,pt):
    ret = {}
    to_visit = [(0,pt)]

    lx = len(maze[0])    
    ly = len(maze)

    deltas = [(0,-1) , (0,1) , (1,0) , (-1,0)]

    seen = set()
    # flood fill
    while to_visit:
        l,(px,py) = to_visit.pop()

        seen.add((px,py))

        for dx,dy in deltas:
            if lx > px + dx >= 0 and ly > py + dy >= 0:
                nx,ny = px+dx,py+dy
                if (nx,ny) in junctions:
                    ret[(nx,ny)] = l + 1
                elif maze[ny][nx] != "#" and (nx,ny) not in seen:
                    to_visit.append((l+1,(nx,ny)))

    del ret[pt]
    return ret

class Mask:
    def __init__(self,junctions):
        self.junctions = list(junctions)
        self.cache = {s:i for i,s in enumerate(junctions)}

    def set_state(self,states,state):
        mask = 0x1 << self.cache[state]

        return states | mask

    def check_state(self,states,state):
        idx = self.cache[state]
        mask = 0x1 << idx

        return ((states & mask) >> idx) == 0x1

@profiler
def part2():
    maze = [list(l.strip()) for l in open("day23/input.txt").readlines()]

    lx = len(maze[0])    
    ly = len(maze)

    start = (maze[0].index(".") ,0)
    end = (maze[-1].index(".") , ly-1)

    junctions = set([start,end])

    deltas = [(0,-1) , (0,1) , (1,0) , (-1,0)]

    for y,l in enumerate(maze):
        for x,c in enumerate(l):
            if c != "#":
                neighbors = 0
                for dx,dy in deltas:
                    if lx > x + dx >= 0 and ly > y + dy >= 0 and maze[y+dy][x+dx] != "#":
                        neighbors += 1

                if neighbors >= 3:
                    junctions.add((x,y))

    reduced_maze = {p:explore_pt(maze,junctions,p) for p in junctions}
    mask = Mask(junctions)
    longest = 0

    start_state = mask.set_state(0,start)
    visited = set([start_state])

    to_visit = [(start,0,start_state)]
    memo = {}

    while to_visit:
        cn,l,cp = to_visit.pop()
        if cn == end:
            longest = max(l,longest)
            continue
        
        if (cn,cp) in memo and memo[(cn,cp)] >= l:
            continue

        memo[(cn,cp)] = l
        
        for n in reduced_maze[cn]:
            if not mask.check_state(cp,n):
                nl = l + reduced_maze[cn][n]
                to_visit.append((n,nl,mask.set_state(cp,n)))

    
    print(longest)

if __name__ == "__main__":
    part1()
    part2()
