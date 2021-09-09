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
        self.prev = self
        self.next = self


def print_table(n):
    visited = False

    while True:
        if n.val == 0:
            if not visited:
                visited = True
            else:
                break
        print(n.val, end=" ")

        n = n.next

    print()


@ profiler
def part_2():
    n_player = 459
    n_marbles = 71320 * 100

    head = node(0)

    scores = [0] * n_player
    next_marble = 1
    current_node = head

    while next_marble < n_marbles:

        tmp_node = node(next_marble)

        if next_marble % 23 != 0:
            current_node = current_node.next

            tmp_node.next = current_node.next
            tmp_node.prev = current_node
            tmp_node.next.prev = tmp_node

            current_node.next = tmp_node
            current_node = tmp_node

        else:
            to_remove = current_node

            for _ in range(7):
                to_remove = to_remove.prev

            scores[(next_marble - 1) % n_player] += next_marble + to_remove.val

            to_remove.prev.next = to_remove.next
            to_remove.next.prev = to_remove.prev

            current_node = to_remove.next

            del(to_remove)
            del(tmp_node)

        next_marble += 1

    print(max(scores))


if __name__ == "__main__":

    part_1()
    part_2()
