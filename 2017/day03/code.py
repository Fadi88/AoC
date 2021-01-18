import time
import math


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        method(*arg, **kw)
        print('Method ' + method.__name__ + ' took : ' +
              "{:2.5f}".format(time.time()-t) + ' sec')
    return wrapper_method

@profiler
def part1():

    inp = 277678

    d = math.ceil(math.sqrt(inp))
    offset = d**2 - inp

    print(int((d-1)/2 + d//2 - offset % (d-1)))


@profiler
def part2():

    inp = 277678

    # https://oeis.org/A141481
    # Square spiral of sums of selected
    # preceding terms, starting at 1.

    series = [
        1, 1, 2, 4, 5, 10, 11, 23, 25, 26, 54, 57, 59, 122, 133, 142, 147, 
        304, 330, 351, 362, 747, 806, 880, 931, 957, 1968, 2105, 2275, 2391, 
        2450, 5022, 5336, 5733, 6155,6444, 6591, 13486, 14267, 15252, 16295, 
        17008, 17370, 35487,37402, 39835, 42452, 45220, 47108, 48065, 98098, 
        103128,109476, 116247, 123363,128204 ,130654 ,266330 ,279138 , 295229,
        312453 ,330785 ,349975 ,363010 ,369601 ,752688 ,787032 ,830037 ,875851 ,
        924406 ,975079 ,1009457 ,1026827 ,2089141 ,2179400 ,2292124 ,2411813 ,
        2539320 ,2674100 ,2814493 ,2909666 ,2957731 ,6013560 ,6262851 ,6573553 ,
        6902404 ,7251490 ,7619304 ,8001525 ,8260383 ,8391037,17048404 ,17724526 ,
        18565223 ,19452043 ,20390510 ,21383723 ,22427493 ,23510079
        ]

    for i in series:
        if i > inp:
            print(i)
            break

if __name__ == "__main__":

    part1()
    part2()
