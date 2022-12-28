from collections import Counter
import time


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print("Method " + method.__name__ + " took : " +
              "{:2.5f}".format(time.time() - t) + " sec")
        return ret

    return wrapper_method


direction = {">": 1, "<": -1, "v": +1j, "^": -1j}


next_turn = [1j ** 3, 1j ** 4, 1j ** 1]


class car:
    def __init__(self, pos, c):
        self.pos = pos
        self.dir = direction[c]
        self.turn_idx = 0

    def __repr__(self):
        return str(self.pos) + " " + str(self.dir)


def plot(grid, cars):
    direction_rev = {1: ">",  -1: "<",  +1j: "v", -1j:  "^"}
    cars_dict = {c.pos: direction_rev[c.dir] for c in cars}

    xs = set(int(g.real) for g in grid.keys())
    ys = set(int(g.imag) for g in grid.keys())

    for y in range(max(ys) + 1):
        for x in range(max(xs) + 1):
            if x+y*1j in cars_dict:
                print(cars_dict[x+y*1j], end="")
            elif x+y*1j in grid:
                print(grid[x+y*1j], end="")
            else:
                print(" ", end="")
        print()
    print()


@profiler
def part_1():
    grid = {}
    cars = []
    for y, l in enumerate(open("day13/input.txt").read().splitlines()):
        for x, c in enumerate(l):
            if c in ["+", "/", "\\", "|", "-"]:
                grid[complex(x, y)] = c
            elif c in ["<", ">"]:
                grid[complex(x, y)] = "-"
                cars.append(car(complex(x, y), c))
            elif c in ["v", "^"]:
                grid[complex(x, y)] = "|"
                cars.append(car(complex(x, y), c))

    while len(cars) == len(set(c.pos for c in cars)):
        cars.sort(key=lambda c: (c.pos.imag, c.pos.real))

        for i in range(len(cars)):

            n_pos = cars[i].pos + cars[i].dir

            if grid[n_pos] == "+":
                cars[i].dir *= next_turn[cars[i].turn_idx]
                cars[i].turn_idx = (cars[i].turn_idx + 1) % len(next_turn)
            elif grid[n_pos] == "\\":
                cars[i].dir = cars[i].dir.imag + cars[i].dir.real*1j
            elif grid[n_pos] == "/":
                cars[i].dir = -cars[i].dir.imag - cars[i].dir.real*1j
            else:
                assert(grid[n_pos] in ["-", "|"])

            if n_pos in [c.pos for c in cars]:
                print(f"{int(n_pos.real)},{int(n_pos.imag)}")
                return
            cars[i].pos = n_pos


@profiler
def part_2():
    grid = {}
    cars = []
    for y, l in enumerate(open("day13/input.txt").read().splitlines()):
        for x, c in enumerate(l):
            if c in ["+", "/", "\\", "|", "-"]:
                grid[complex(x, y)] = c
            elif c in ["<", ">"]:
                grid[complex(x, y)] = "-"
                cars.append(car(complex(x, y), c))
            elif c in ["v", "^"]:
                grid[complex(x, y)] = "|"
                cars.append(car(complex(x, y), c))

    while len(cars) > 1:
        cars.sort(key=lambda c: (c.pos.imag, c.pos.real))

        to_remove = set()

        for i in range(len(cars)):

            n_pos = cars[i].pos + cars[i].dir

            if grid[n_pos] == "+":
                cars[i].dir *= next_turn[cars[i].turn_idx]
                cars[i].turn_idx = (cars[i].turn_idx + 1) % len(next_turn)
            elif grid[n_pos] == "\\":
                cars[i].dir = cars[i].dir.imag + cars[i].dir.real*1j
            elif grid[n_pos] == "/":
                cars[i].dir = -cars[i].dir.imag - cars[i].dir.real*1j
            else:
                assert(grid[n_pos] in ["-", "|"])

            if n_pos in [c.pos for c in cars]:
                to_remove.add(i)
                to_remove.add([i for i,c in enumerate(cars) if c.pos == n_pos][0])
                
            cars[i].pos = n_pos

        l = list(to_remove)
        l.sort(reverse=True)
        for i in l:
            del cars[i]

    pos = cars[0].pos
    print(f"{int(pos.real)},{int(pos.imag)}")

if __name__ == "__main__":

    part_1()
    part_2()
