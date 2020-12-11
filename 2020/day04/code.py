import time,os,re

def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        method(*arg, **kw)
        print('Method '  + method.__name__ +' took : ' + "{:2.5f}".format(time.time()-t) + ' sec')
    return wrapper_method

@profiler
def part1():

    pass_list = []
    with open('input.txt', 'r') as f_in:
        pass_list = [tmp.replace('\n' , ' ')for tmp in f_in.read().split('\n\n')]

        cnt = 0

        for item in pass_list:
            if   item.count('byr') == 1 and item.count('iyr') == 1 and item.count('eyr') == 1  and item.count('hgt') == 1 and \
                 item.count('hcl') == 1 and item.count('ecl') == 1 and item.count('pid') == 1 :
                cnt += 1
        print('part 1 answer : ' , cnt)


@profiler
def part2():

    pass_list = []
    with open('input.txt', 'r') as f_in:

        cnt = 0
        pass_list = [tmp.replace('\n' , ' ') for tmp in f_in.read().split('\n\n')]

        for item in pass_list:

            if    item.count('byr') == 1 and item.count('iyr') == 1 and item.count('eyr') == 1  and item.count('hgt') == 1 and \
                  item.count('hcl') == 1 and item.count('ecl') == 1 and item.count('pid') == 1 :
                checker = {tmp.split(':')[0]:tmp.split(':')[1] for tmp in item.split()}

                if  1920 <= int(checker['byr']) <= 2002 and \
                2010 <= int(checker['iyr']) <= 2020 and \
                2020 <= int(checker['eyr']) <= 2030 and \
                re.match(r'#[0-9a-f]{6}$' , checker['hcl'] ) and \
                re.match(r'[0-9]{9}$' , checker['pid'] )  and\
                checker['ecl'] in ['amb','blu','brn','gry','grn','hzl','oth']:

                    if ( 'cm' in checker['hgt'] and 150 <= int(checker['hgt'][:-2]) <= 193) or \
                        ('in' in checker['hgt'] and 59  <= int(checker['hgt'][:-2]) <= 76 )    :
                        cnt += 1
 
        print('part 2 answer : ' , cnt )

if __name__ == "__main__":

    part1()
    part2()
