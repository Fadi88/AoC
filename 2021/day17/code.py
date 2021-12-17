import time
import re
import math


def profiler(method):
    def wrapper_method(*arg, **kw):
        t_0 = time.time()
        ret = method(*arg, **kw)
        new_t = time.time() - t_0
        print("Method " + method.__name__ + " took : " + f"{new_t:2.5f}" + " sec")
        return ret

    return wrapper_method


def get_pos(vx0, vy0, current_time):
    current_y = vy0 * current_time - (current_time - 1) * (current_time) // 2

    # ignore -ve x as the input is to the right
    current_x = (
        (2 * vx0 - current_time + 1) * (current_time) // 2
        if current_time < vx0
        else vx0 * (vx0 + 1) // 2
    )

    return current_x, current_y


def will_intersect(current_v, upper_bound, lower_bound):
    # get time limit based on y because it is easier to get than x
    # if it works for that time slot for y should also work x
    # because they both has to match
    tmin = math.floor(
        current_v[1] + math.sqrt(current_v[1] * current_v[1] - 2 * upper_bound[1])
    )
    tmax = math.floor(
        current_v[1] + math.sqrt(current_v[1] * current_v[1] - 2 * lower_bound[1])
    )

    for current_t in range(tmin, tmax + 2):
        current_x, current_y = get_pos(current_v[0], current_v[1], current_t)
        if (
            upper_bound[0] <= current_x <= lower_bound[0]
            and lower_bound[1] <= current_y <= upper_bound[1]
        ):
            return True
    return False


@profiler
def part1():
    with open("day17/input.txt", encoding="utf-8") as f_d:
        _, _, y_1, _ = list(map(int, re.findall(r"-?\d+", f_d.read())))

    print(abs(y_1) * (abs(y_1) - 1) // 2)


@profiler
def part2():
    with open("day17/input.txt", encoding="utf-8") as f_d:
        x_1, x_2, y_1, y_2 = list(map(int, re.findall(r"-?\d+", f_d.read())))

    # assume area is under y = 0

    # bounds if exceeded after 1 second will overshoot
    vy_min = y_1
    vx_max = x_2

    vy_max = -y_1
    vx_min = math.floor(math.sqrt(2 * x_1) - 1)

    upper_bound = (x_1, y_2)
    lower_bound = (x_2, y_1)

    tmp = sum(
        [
            will_intersect((vx, vy), upper_bound, lower_bound)
            for vx in range(vx_min, vx_max + 1)
            for vy in range(vy_min, vy_max + 1)
        ]
    )

    print(tmp)


if __name__ == "__main__":

    part1()
    part2()
