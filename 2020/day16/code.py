import time,os
import re

def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print('Method '  + method.__name__ +' took : ' + "{:2.5f}".format(time.time()-t) + ' sec')
        return ret
    return wrapper_method


def check_valid_rule(val,rule):
    return not( rule[0][1] <= val <= rule[0][1] or rule[0][1] <= val <= rule[0][1])

@profiler
def part1():
    rules = []
    comb_rules = set()
    my_ticket = []
    other_tickets = []

    for l in open('input.txt', 'r').read().split('\n'):
        if 'or' in l:
            vals = [*map(int, re.findall(r'(\d+)' , l))]
            rules.append(((vals[0] , vals[1]) , (vals[2] , vals[3])))
            comb_rules.update(set(range(vals[0] , vals[1] + 1)))
            comb_rules.update(set(range(vals[2] , vals[3] + 1)))

        elif re.match(r'^(\d+,){19}\d+$' , l ):
            vals = [*map(int, re.findall(r'(\d+)' , l))]
            if len(my_ticket) != 0:
                other_tickets.append(vals)
            else:
                my_ticket = vals

    cnt = 0
    for tik in other_tickets:
        for val in tik:
            if val not in comb_rules:
                cnt += val

    print(cnt)

@profiler
def part2():
    comb_rules = set()
    rule_map = {}
    my_ticket = []
    other_tickets = []

    for l in open('input.txt', 'r').read().split('\n'):
        if 'or' in l:
            vals = [*map(int, re.findall(r'(\d+)' , l))]
            comb_rules.update(set(range(vals[0] , vals[1] + 1)))
            comb_rules.update(set(range(vals[2] , vals[3] + 1)))
            rule_map[l[:l.find(':') ]] = set(range(vals[0] , vals[1] + 1)) | set(range(vals[2] , vals[3] + 1))

        elif re.match(r'^(\d+,){19}\d+$' , l ):
            vals = [*map(int, re.findall(r'(\d+)' , l))]
            if len(my_ticket) != 0:
                other_tickets.append(vals)
            else:
                my_ticket = vals

    valid_tickets = []
    for tik in other_tickets:
        valid_ticket = True

        for val in tik:
            if val not in comb_rules:
                valid_ticket = False
                break

        if valid_ticket:
            valid_tickets.append(tik)

    pos = {}
    for i in range(len(my_ticket)):
        pos[i] = set(rule_map.keys())

    for tik in valid_tickets:
        for idx,val in enumerate(tik):
            for rule in rule_map:
                if val not in rule_map[rule]:
                    pos[idx].remove(rule)
 
    pos_prob = {}
    for tmp in pos :
        pos_prob[len(pos[tmp])] = tmp

    for i in range(len(pos)):
        field = list(pos[pos_prob[i+1]])[0]
        for rule in pos:
            if len(pos[rule]) > 1:
                pos[rule].remove(field)

    departure_idx_map = {}
    for tmp in pos:
        field = pos[tmp].pop()
        if field.startswith('departure'):
            departure_idx_map[field] = tmp

    prod = 1
    for idx in departure_idx_map.values():
        prod *= my_ticket[idx]

    print(prod)
        

if __name__ == "__main__":

    part1()
    part2()
