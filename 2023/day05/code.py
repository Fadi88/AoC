from time import perf_counter

# pylint: disable=C0209,C0206,C0201,C0103,C0116,W1514


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print("Method " + method.__name__ + " took : " + "{:2.5f}".format(perf_counter() - t) + " sec")
        return ret

    return wrapper_method


@profiler
def part1():
    Ts = open("day05/input.txt").read().split("\n\n")

    seeds = list(map(int, Ts[0].split(":")[1].strip().split()))
    T = {}

    for t in Ts[1:]:
        p = t.splitlines()
        k = tuple(p[0].split()[0].split("-to-"))
        T[k] = []

        for m in p[1:]:
            T[k].append(list(map(int, m.split())))

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

    seeds = list(map(int, Ts[0].split(":")[1].strip().split()))
    T = {}

    for t in Ts[1:]:
        p = t.splitlines()
        k = tuple(p[0].split()[0].split("-to-"))
        T[k] = []

        for c_map in p[1:]:
            T[k].append(list(map(int, c_map.split())))

    current_state = "seed"

    while current_state != "location":
        for state in T.keys():
            if state[0] == current_state:
                current_state = state[1]
                mappings = T[state]
                break

        to_map = []
        for i in range(len(seeds) // 2):
            loc = seeds[2 * i]
            rng = seeds[2 * i + 1]
            to_map.append((loc, rng))

        new_seeds = []
        while to_map:
            loc, rng = to_map.pop(0)
            mapped = False
            for c_map in mappings:
                c_src_beg = c_map[1]
                c_src_end = c_map[1] + c_map[2]
                c_dst_ref = c_map[0]

                if (
                    c_src_beg <= loc <= c_src_end
                    or c_src_beg <= loc + rng <= c_src_end
                    or loc <= c_src_beg <= loc + rng
                    or loc <= c_src_end <= loc + rng
                ):
                    n_l = max(loc, c_src_beg)
                    n_e = min(loc + rng, c_src_end)
                    new_seeds += [c_dst_ref + (n_l - c_src_beg), n_e - n_l]
                    if loc < c_src_beg:
                        to_map.append((loc, c_src_beg - loc - 1))
                    if loc + rng > c_src_end:
                        to_map.append((c_src_end + 1, (loc + rng) - c_src_end))
                    mapped = True
                    break
            if not mapped:
                new_seeds += [loc, rng]

        seeds = new_seeds
    print(min([seeds[2 * i] for i in range(len(seeds) // 2)]))


if __name__ == "__main__":
    part1()
    part2()
