import time,re

def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print('Method '  + method.__name__ +' took : ' + "{:2.5f}".format(time.time()-t) + ' sec')
        return ret
    return wrapper_method


def replace(match_obj):
    s = match_obj.group(1)
    return str(len(s)) + s[0]

@profiler
def part1():

    pswd = '3113322113'

    for _ in range(40):
        val = re.sub(r'((\d)\2*)',replace,val)
        
    print(len(val))


@profiler
def part2():
    val = '3113322113'

    for _ in range(50):
        val = re.sub(r'((\d)\2*)',replace,val)
        
    print(len(val))


if __name__ == "__main__":

    part1()
    part2()
