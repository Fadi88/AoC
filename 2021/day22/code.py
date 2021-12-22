import time
import re


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print(
            "Method "
            + method.__name__
            + " took : "
            + "{:2.5f}".format(time.time() - t)
            + " sec"
        )
        return ret

    return wrapper_method


@profiler
def part1():
    cubes = set()
    for l in open("day22/input.txt").read().split("\n"):
        coor = list(map(int, re.findall(r"-?\d+", l)))
        assert coor[1] >= coor[0]
        assert coor[3] >= coor[2]
        assert coor[5] >= coor[4]
        if (
            coor[0] > 50
            or coor[1] < -50
            or coor[2] > 50
            or coor[3] < -50
            or coor[4] > 50
            or coor[5] < -50
        ):
            continue
        if "on" in l:
            for x in range(max(coor[0], -50), min(50, coor[1]) + 1):
                for y in range(max(coor[2], -50), min(50, coor[3]) + 1):
                    for z in range(max(coor[4], -50), min(50, coor[5]) + 1):
                        cubes.add((x, y, z))
        else:
            for x in range(max(coor[0], -50), min(50, coor[1]) + 1):
                for y in range(max(coor[2], -50), min(50, coor[3]) + 1):
                    for z in range(max(coor[4], -50), min(50, coor[5]) + 1):
                        if (x, y, z) in cubes:
                            cubes.remove((x, y, z))

    print(len(cubes))


def does_line_intersect(x0, x1, ox0, ox1):
    return x0 < ox0 < x1 or x0 < ox1 < x1 or ox0 < x0 < ox1 or  ox0 < x1 < ox1


def get_line_intersection(p0, p1, op0, op1):
    assert does_line_intersect(p0, p1, op0, op1)
    r0 = p0 if op0 < p0 else op0
    r1 = op1 if op1 < p1 else p1

    return r0, r1


class cubiod:
    def __init__(self, x0, x1, y0, y1, z0, z1) -> None:
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1
        self.z0 = z0
        self.z1 = z1

        self.off = []

    def is_intersecting(self, other):
        return (
            does_line_intersect(self.x0, self.x1, other.x0, other.x1)
            and does_line_intersect(self.y0, self.y1, other.y0, other.y1)
            and does_line_intersect(self.z0, self.z1, other.z0, other.z1)
        )

    def substraction(self, other):
        if self.is_intersecting(other):
            x = get_line_intersection(self.x0, self.x1, other.x0, other.x1)
            y = get_line_intersection(self.y0, self.y1, other.y0, other.y1)
            z = get_line_intersection(self.z0, self.z1, other.z0, other.z1)

            for o in self.off:
                o.substraction(other)

            self.off.append(cubiod(x[0], x[1], y[0], y[1], z[0], z[1]))

    def volume(self):
        return (
            (self.x1 - self.x0 + 1) * (self.y1 - self.y0 + 1) * (self.z1 - self.z0 + 1)
            - sum([c.volume() for c in self.off])
        )

    def __str__(self) -> str:
        ret = "" + str(self.x0) + ", " + str(self.x1) + ", " + str(self.y0) + ", "
        ret += str(self.y1) + ", " + str(self.z0) + ", " + str(self.z1)

        return ret


@profiler
def part2():
    cubiods = []

    for l in open("day22/input.txt").read().split("\n"):
        (x0, x1, y0, y1, z0, z1) = tuple(map(int, re.findall(r"-?\d+", l)))

        n_cube = cubiod(x0, x1, y0, y1, z0, z1)
        for c in cubiods:
            c.substraction(n_cube)
        if "on" in l:
            cubiods.append(n_cube)


    print(sum([c.volume() for c in cubiods]))


if __name__ == "__main__":

    part1()
    part2()
