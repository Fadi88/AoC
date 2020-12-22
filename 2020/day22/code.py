import time,os,re

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
        if str(game[1]) + str(game[2]) not in seen :
            seen.add(str(game[1]) + str(game[2]))
        else :
            game[2].clear()
            return game

        p1 = game[1].pop(0)
        p2 = game[2].pop(0)

        if len(game[1]) >= p1 and len(game[2]) >= p2:
            tmp = {}
            tmp[1] = game[1][:p1+1]
            tmp[2] = game[2][:p2+1]
            tmp = play_game(tmp)

            if len(tmp[2]) == 0:
                game[1].append(p1)
                game[1].append(p2)
            elif len(tmp[2]):
                game[2].append(p2)
                game[2].append(p1)
            else :
                assert False

        else :
            if p1 > p2:
                game[1].append(p1)
                game[1].append(p2)
            elif p1 < p2 :
                game[2].append(p2)
                game[2].append(p1)
            else :
                assert False

    return game

@profiler
def part1():

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

    round = 0
    while len(game[1]) != 0 and len(game[2]) != 0 :
        round += 1
        p1 = game[1].pop(0)
        p2 = game[2].pop(0)

        if p1 > p2:
            game[1].append(p1)
            game[1].append(p2)
        elif p1 < p2 :
            game[2].append(p2)
            game[2].append(p1)

    l = game[1] if len(game[1]) > 0 else game[2]

    score = 0
    for i,c in enumerate(l[::-1]):
        score += ( c * (i + 1))

    print(round , score)

@profiler
def part2():

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

    game = play_game(game)

    l = game[1] if len(game[1]) > 0 else game[2]

    score = 0
    for i,c in enumerate(l[::-1]):
        score += ( c * (i + 1))

    print(cnt , score)

if __name__ == "__main__":

    part1()
    part2()
