import time,re

def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print('Method '  + method.__name__ +' took : ' + "{:2.5f}".format(time.time()-t) + ' sec')
        return ret
    return wrapper_method


def next_pass(s):
    idx = 1
    s = list(s)
    while True:
        ch = s[-idx]
        if ch == 'z':
            s[-idx] = 'a'
            idx += 1
        else :
            s[-idx] = chr(ord(ch) + 1)
            break

    return ''.join(s)

def is_valid(pswd):
    invalid_char = 'i' in pswd or 'o' in pswd or 'l' in pswd
    three_seq = any([ ord(pswd[i-1]) + 1 == ord(pswd[i]) == ord(pswd[i+1]) - 1 for i in range(1,len(pswd) -1)])
    has_2_pair = re.match(r'.*(\w)\1.*([^\1])\2.*',pswd) is not None

    return not invalid_char and three_seq and has_2_pair

@profiler
def part1():

    pswd = 'hxbxwxba'
    while True:
        if is_valid(pswd):
            break
        pswd = next_pass(pswd)

    print(pswd)

@profiler
def part2():

    pswd = 'hxbxwxba'
    while True:
        if is_valid(pswd):
            break
        pswd = next_pass(pswd)

    pswd = next_pass(pswd)

    while True:
        if is_valid(pswd):
            break
        pswd = next_pass(pswd)

    print(pswd)



if __name__ == "__main__":

    part1()
    part2()
