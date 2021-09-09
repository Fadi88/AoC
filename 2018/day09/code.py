import time


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print('Method ' + method.__name__ + ' took : ' +
              "{:2.5f}".format(time.time()-t) + ' sec')
        return ret
    return wrapper_method


@profiler
def part_1():
    n_player = 459
    n_marbles = 71320

    circle = [0]
    scores = [0] * n_player
    next_marble = 0
    current_idx = 0

    while next_marble < n_marbles:
        next_marble += 1

        if next_marble % 23 != 0:
            current_idx = (current_idx + 2) % len(circle)
            circle.insert(current_idx + 1, next_marble)
        else:
            tmp = (current_idx-6) % len(circle)
            scores[(next_marble - 1) %
                   n_player] += next_marble + circle.pop(tmp)
            current_idx = tmp - 1

    print(max(scores))


class node:
    def __init__(self, v) -> None:
        self.val = v
        self.prev = None
        self.next = None


@ profiler
def part_2():
    n_player = 9
    n_marbles = 25

    head = node(0)
    head.next = head
    head.prev = head

    scores = [0] * n_player
    next_marble = 0
    current_marble = head

    while next_marble < n_marbles:
        next_marble += 1
        tmp_node = node(next_marble)
        if next_marble % 23 != 0:
            current_node = current_marble.next.next

            tmp_node.next = current_node.next
            current_node.next = tmp_node
            tmp_node.prev = current_node
            current_node = tmp_node

        else:
            tmp_node = current_marble.prev.prev.prev.prev.prev.prev.prev

            scores[(next_marble - 1) % n_player] += next_marble + tmp_node.val

            tmp_node.prev.next = tmp_node.next
            tmp_node.next.prev = tmp_node.prev

            del(tmp_node)

    tmp = head.next
    while (tmp.val != 0):
        print(tmp.val, end=" ")
        tmp = tmp.next
    print(scores)


if __name__ == "__main__":

    part_1()
    part_2()
