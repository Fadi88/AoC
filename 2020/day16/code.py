import time,os,re,operator
from functools import reduce

def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        method(*arg, **kw)
        print('Method '  + method.__name__ +' took : ' + "{:2.5f}".format(time.time()-t) + ' sec')
    return wrapper_method

@profiler
def part1():
    comb_rules = set()
    other_tickets = []

    for l in open('input.txt', 'r').read().split('\n'):
        if 'or' in l:
            vals = list(map(int, re.findall(r'(\d+)' , l)))
            comb_rules |= set(range(vals[0] , vals[1] + 1)) | set(range(vals[2] , vals[3] + 1))

        elif ',' in l : other_tickets.append(list(map(int , l.split(','))))

    print(sum([val for tik in other_tickets for val in tik if val not in comb_rules]))

@profiler
def part2():
    comb_rules = set()
    rule_map = {}
    other_tickets = []

    for l in open('input.txt', 'r').read().split('\n'):
        if 'or' in l:
            vals = list(map(int, re.findall(r'(\d+)' , l)))
            comb_rules |= set(range(vals[0] , vals[1] + 1)) | set(range(vals[2] , vals[3] + 1))
            rule_map[l[:l.find(':') ]] = set(range(vals[0] , vals[1] + 1)) | set(range(vals[2] , vals[3] + 1))

        elif ',' in l :  other_tickets.append(list(map(int , l.split(','))))

    pos = { i : set(rule_map.keys()) for i in range(len(other_tickets[0])) }

    for tik in other_tickets:
        if any([val not in comb_rules for val in tik]) : continue

        for idx,val in enumerate(tik):
            for rule in rule_map:
                if val not in rule_map[rule] : pos[idx].remove(rule)

    visited = [False for _ in range(len(pos))]

    for _ in range(len(pos)):
        for idx in pos:
            if len(pos[idx]) == 1 and not visited[idx]:
                visited[idx] = True
                target_idx = idx
                target_field = [e for e in pos[idx]][0]
                break

        for idx in pos:
            if idx == target_idx : continue
            if target_field in pos[idx] : pos[idx].remove(target_field)

    print(reduce(operator.mul , [ other_tickets[0][i] for i in pos if 'departure' in pos[i].pop()]))

if __name__ == "__main__":

    part1()
    part2()
