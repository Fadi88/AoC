import time,os
import re

def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print('Method '  + method.__name__ +' took : ' + "{:2.5f}".format(time.time()-t) + ' sec')
        return ret
    return wrapper_method

@profiler
def part1():

    rules_parse = {}
    msgs = []
    for l in open('input.txt', 'r').read().split('\n'):
        if ':' in l:
            p = l.split(':')
            rules_parse[p[0]] = p[1].strip()
            
        elif 'a' in l or 'b' in l :
            msgs.append(l)
    
    rules_done = {}
    while '0' not in rules_done:
        for ele in rules_parse:
            if ele in rules_done : continue

            if '"' in rules_parse[ele]:
                rules_done[ele] = rules_parse[ele].replace('"' , '')

            else :
                nums = re.findall(r'(\d+)' , rules_parse[ele])
                nums.sort(key=len,reverse=True)
            
                if (all([num in rules_done for num in nums])):
                    for num in nums:
                        rules_parse[ele] = re.sub(num ,rules_done[num], rules_parse[ele])
                    
                    rules_parse[ele] = rules_parse[ele].replace(' ' , '')
                    if '|' in rules_parse[ele] :
                        rules_parse[ele] = '(' + rules_parse[ele] +')'
                    rules_done[ele] = rules_parse[ele]

    return sum([bool(re.fullmatch(rules_done['0'].replace('x' , str(1)) , msg)) for msg in msgs])

@profiler
def part2():

    rules_parse = {}
    msgs = []
    for l in open('input.txt', 'r').read().split('\n'):
        if ':' in l:
            p = l.split(':')
            rules_parse[p[0]] = p[1].strip()
            
        elif 'a' in l or 'b' in l :
            msgs.append(l)

    rules_done = {}
    while '0' not in rules_done:
        for ele in rules_parse:
            if ele in rules_done : continue

            if '"' in rules_parse[ele]:
                rules_done[ele] = rules_parse[ele].replace('"' , '')

            else :
                nums = re.findall(r'(\d+)' , rules_parse[ele])
                nums.sort(key=len,reverse=True)

                if ele == '8' and '42' in rules_done:
                    rules_done[ele] = rules_done['42'] + '+'
                elif ele == '11' and '42' in rules_done and '31' in rules_done:
                    rules_done[ele] = rules_done['42'] + r'{x}' + rules_done['31'] + r'{x}'
            
                elif (all([num in rules_done for num in nums])):
                    for num in nums:
                        rules_parse[ele] = re.sub(num ,rules_done[num], rules_parse[ele])
                    
                    rules_parse[ele] = rules_parse[ele].replace(' ' , '')
                    if '|' in rules_parse[ele] :
                        rules_parse[ele] = '(' + rules_parse[ele] +')'
                    rules_done[ele] = rules_parse[ele]

    cnt = sum([bool(re.fullmatch(rules_done['0'].replace('x' , str(1)) , msg)) for msg in msgs])
    print(rules_done['0'])
    prv_cnt = 0
    rep = 2
    while prv_cnt != cnt:
        prv_cnt = cnt
        cnt += sum([bool(re.fullmatch(rules_done['0'].replace('x' , str(rep)) , msg)) for msg in msgs])
        rep +=1

    return cnt

if __name__ == "__main__":

    print(part1())
    print(part2())
