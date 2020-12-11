import time,os

def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print('Method '  + method.__name__ +' took : ' + "{:2.5f}".format(time.time()-t) + ' sec')
        return ret
    return wrapper_method

@profiler
def part1():

    pre_len = 25

    with open('input.txt', 'r') as f_in:
        input = [int(l) for l in f_in]

        for i in range(pre_len, len(input)):
            found = False
            for a in range(i -  pre_len, i):
                for b in range( a + 1 , i ):
                    if input[a] + input[b] == input[i]:
                        found = True
                        break
                if found :
                    break
            if not found:
                print('part 1 answer : ' , input[i])
                return input[i]


@profiler
def part2(target):
    with open('input.txt', 'r') as f_in:
        input = [int(l) for l in f_in]

        for i in range(len(input)):
            sum = input[i]
            ls = [input[i]]
            wrong_seq = False

            for a in range(i+1 , len(input)):
                sum += input[a]
                ls.append(input[a])
                if sum > target :
                    wrong_seq = True
                    break
                elif sum == target:
                    print('part 2 answer : ' , min(ls) + max(ls))
                    return

            if wrong_seq:
                continue


if __name__ == "__main__":
    

    target = part1()
    part2(target)

    
    