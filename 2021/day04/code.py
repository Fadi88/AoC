import time


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print('Method ' + method.__name__ + ' took : ' +
              "{:2.5f}".format(time.time()-t) + ' sec')
        return ret
    return wrapper_method


def get_baord_sum(board):
    return sum([sum(filter(None, l)) for l in board])


@profiler
def part1():
    content = open('input.txt').read().split('\n\n')

    nums = list(map(int, content[0].split(',')))
    boards = [[list(map(int, l.split())) for l in board.split('\n')]
              for board in content[1:]]

    for num in nums:
        # remove seleceted numbers from all boards
        for board in boards:
            for l in board:
                if num in l:
                    l[l.index(num)] = None

        # check all boards for marked lines
        for board in boards:
            score = []

            for l in board:
                if all(i is None for i in l):
                    score.append(get_baord_sum(board)*num)

            for i in range(len(board[0])):
                if all(l[i] is None for l in board):
                    score.append(get_baord_sum(board)*num)

            if len(score) > 0:
                print("part 1 : ", score[0])

                return


@profiler
def part2():
    content = open('input.txt').read().split('\n\n')

    nums = list(map(int, content[0].split(',')))
    boards = [[list(map(int, l.split())) for l in board.split('\n')]
              for board in content[1:]]

    score = []
    for num in nums:
        # remove seleceted numbers from all boards
        for board in boards:
            for l in board:
                if num in l:
                    l[l.index(num)] = None

        # check all boards for marked lines
        for board in boards:

            for l in board:
                if all(i is None for i in l):
                    score.append(get_baord_sum(board)*num)
                    if board in boards:
                        boards.remove(board)

            for i in range(len(board[0])):
                if all(l[i] is None for l in board):
                    score.append(get_baord_sum(board)*num)
                    if board in boards:
                        boards.remove(board)

    print("part 2 : ", score[-1])


if __name__ == "__main__":

    part1()
    part2()
