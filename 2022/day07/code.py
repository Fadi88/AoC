from time import perf_counter
from collections import defaultdict
from pathlib import Path


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print('Method ' + method.__name__ + ' took : ' +
              "{:2.5f}".format(perf_counter()-t) + ' sec')
        return ret
    return wrapper_method


def get_folder_size():
    current_path = ""
    file_size = {}

    for l in open("input.txt").readlines():
        if "$" in l:
            if " cd " in l:

                if l.split()[2] == "/":
                    current_path = "/"
                elif l.split()[2] == "..":
                    current_path = current_path.rsplit("/", 1)[0]
                else:
                    current_path += "/" + l.split()[2]
                    current_path = current_path.replace("//", "/")
        else:
            if "dir" not in l:
                file_path = (current_path + "/" + l.split()
                             [1]).replace("//", "/")
                file_size[file_path] = int(l.split()[0])

    folder_size = defaultdict(int)
    for f in file_size:
        folder = Path(f).parent
        while True:
            folder_size[folder] += file_size[f]
            if folder == Path("/"):
                break
            folder = folder.parent

    return folder_size


@profiler
def part1():
    folder_size = get_folder_size()

    print(sum(filter(lambda x: x <= 100000, folder_size.values())))


@profiler
def part2():
    folder_size = get_folder_size()

    total_space = 70000000
    needed_space = 30000000

    least_del = needed_space - (total_space - folder_size[Path("/")])

    for s in sorted(folder_size.values()):
        if s > least_del:
            print(s)
            break


if __name__ == "__main__":

    part1()
    part2()
