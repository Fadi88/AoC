import time,os,re
from copy import deepcopy

def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print('Method '  + method.__name__ +' took : ' + "{:2.5f}".format(time.time()-t) + ' sec')
        return ret
    return wrapper_method

cnt = 0
def play_game(game):
    
    global cnt
    seen = set()
    cnt += 1

    while len(game[1]) != 0 and len(game[2]) != 0 :
        key = str(game[1]) + str(game[2])
        if key not in seen :
            seen.add(key)
        else :
            game[2].clear()
            break

        p1 = game[1].pop(0)
        p2 = game[2].pop(0)

        if len(game[1]) >= p1 and len(game[2]) >= p2:
            tmp = {}
            tmp[1] = game[1][:p1+1]
            tmp[2] = game[2][:p2+1]
            tmp = play_game(tmp)

            if len(tmp[2]) == 0:
                game[1].extend([p1 , p2])
            elif len(tmp[2]):
                game[2].extend([p2 , p1])
            else :
                assert False

        else :
            if p1 > p2:
                game[1].extend([p1 , p2])
            elif p1 < p2 :
                game[2].extend([p2 , p1])
            else :
                assert False
    return game

@profiler
def part1(game):

    round = 0
    while len(game[1]) != 0 and len(game[2]) != 0 :
        round += 1
        p1 = game[1].pop(0)
        p2 = game[2].pop(0)

        if p1 > p2:
            game[1].extend([p1 , p2])
        elif p1 < p2 :
            game[2].extend([p2 , p1])
        else :
            assert False

    l = game[1] if len(game[1]) > 0 else game[2]

    print(round , sum([c * (i+1) for i,c in enumerate(l[::-1])]), len(game[1]) > 0)

@profiler
def part2(game):

    game = play_game(game)
    l = game[1] if len(game[1]) > 0 else game[2]
    print(cnt , sum([c * (i+1) for i,c in enumerate(l[::-1])]) , len(game[1]) > 0)

if __name__ == "__main__":

    game = {}
    game[1] = []
    game[2] = []

    for l in open('input.txt'):
        l = l.strip()
        if 'Player' in l :
            player = re.findall(r'\d+',l)[0]
        else :
            card = re.findall(r'\d+',l)
            if len(card) == 1:
                game[int(player)].append(int(card[0]))

    part1(deepcopy(game))
    part2(deepcopy(game))
