import time,os,re

def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print('Method '  + method.__name__ +' took : ' + "{:2.5f}".format(time.time()-t) + ' sec')
        return ret
    return wrapper_method

target_color = 'shiny gold'

bags = {}
bags_count = {}

def contains_target(color):
    if color is None or bags[color] is None:
        return False
    elif target_color in bags[color] :
        return True
    else:
        return any(map(contains_target , bags[color]))

@profiler
def part1():

    with open('input.txt', 'r') as f_in:
        for l in f_in:
            color = re.search(r'^\w+ \w+' , l)
            if 'no other bags' in l:
                bags[color.group(0)] = None
            else:
                bags[color.group(0)] =re.findall(r'\d+ (\w+ \w+)' , l)
                bags_count[color.group(0)] = list(map(int,re.findall(r'(\d+)' , l)))

        cnt = 0
        for bag_color in bags:
            if contains_target(bag_color):
                cnt += 1

        print('part 1 answer : ' , cnt)

def get_content_count(color):
    cnt = 0

    for cr_cnt , cr_color in zip(bags_count[color] , bags[color]):

        if cr_color in bags and bags[cr_color] is not None:
            cnt += cr_cnt + cr_cnt * get_content_count(cr_color)
        else :
            cnt += cr_cnt

    return cnt


@profiler
def part2():
    print('part 2 answer : ' , get_content_count(target_color)) 
 

if __name__ == "__main__":

    part1()
    part2()
