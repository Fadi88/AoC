from time import perf_counter


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print('Method ' + method.__name__ + ' took : ' +
              "{:2.5f}".format(perf_counter()-t) + ' sec')
        return ret
    return wrapper_method


@profiler
def part1():
    Ts = open("day05/input.txt").read().split("\n\n")

    seeds = list(map(int,Ts[0].split(":")[1].strip().split()))
    T = {}

    for t in Ts[1:]:
        p = t.splitlines()
        k = tuple(p[0].split()[0].split("-to-"))
        T[k] = []

        for m in p[1:]:
            T[k].append(list(map(int,m.split())))

    current_state = "seed"

    while current_state != "location":
        for state in T.keys():
            if state[0] == current_state:
                current_state = state[1]
                ms = T[state]
                break
 
        mapped = {}
        for s in seeds:
            for m in ms:
                if m[1] <= s <= m[1] + m[2]:
                    mapped[s] = m[0] + (s - m[1])
                    break
            if s not in mapped:
                mapped[s] = s
        seeds = list(mapped.values())
     
    print(min(seeds))


@profiler
def part2():
    Ts = open("day05/input.txt").read().split("\n\n")

    seeds = list(map(int,Ts[0].split(":")[1].strip().split()))
    T = {}

    for t in Ts[1:]:
        p = t.splitlines()
        k = tuple(p[0].split()[0].split("-to-"))
        T[k] = []

        for m in p[1:]:
            T[k].append(list(map(int,m.split())))

    current_state = "seed"

    while current_state != "location":
        for state in T.keys():
            if state[0] == current_state:
                current_state = state[1]
                ms = T[state]
                break

        to_map = []
        for i in range(len(seeds)//2):
            l = seeds[2*i]
            r = seeds[2*i +1]
            to_map.append((l,r))

        new_seeds = []
        while to_map:
            l,r = to_map.pop(0)
            mapped = False
            for m in ms:
                if m[1] <= l <= m[1] + m[2] or m[1] <= l+r <= m[1] + m[2] or l <= m[1] <= l+r or l <= m[1] + m[2] <= l+r:
                    n_l = max(l,m[1])
                    n_e = min(l+r,m[1] + m[2])
                    new_seeds += [m[0]+(n_l - m[1]), n_e - n_l]
                    if l < m[1]:
                        to_map.append((l,m[1]-l-1))
                    if l+r > m[1] + m[2]:
                        to_map.append((m[1] + m[2] +1, (l+r) - (m[1] + m[2])))
                    mapped = True
                    break
            if not mapped:
                new_seeds += [l,r]
            
        seeds = new_seeds
    print(min([seeds[2*i] for i in range(len(seeds)//2)]))


if __name__ == "__main__":

    part1()
    part2()
