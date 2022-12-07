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


@profiler
def part1():
    current_path = ""
    file_size = {}

    for l in open("input.txt").readlines():
        if "$" in l:
            if " cd " in l:
                if l.split()[2] not in ["..", "/"]:
                    current_path += ("/" if current_path !=
                                     "/" else "") + l.split()[2]
                elif l.split()[2] == "..":
                    if current_path.count("/") > 0:
                        current_path = current_path.rsplit("/", 1)[0]
                elif l.split()[2] == "/":
                    current_path = "/"
        else:
            if "dir" not in l:
                file_size[(current_path + "/" if len(current_path) >
                           1 else "/") + l.split()[1]] = int(l.split()[0])

    folder_size = defaultdict(int)
    for f in file_size:
        folder = Path(f).parent
        while True:
            folder_size[folder] += file_size[f]
            if folder == Path("/"):
                break
            folder = folder.parent

    print(sum(filter(lambda x: x <= 100000, folder_size.values())))


@profiler
def part2():
    current_path = ""
    file_size = {}

    for l in open("input.txt").readlines():
        if "$" in l:
            if " cd " in l:
                if l.split()[2] not in ["..", "/"]:
                    current_path += ("/" if current_path !=
                                     "/" else "") + l.split()[2]
                elif l.split()[2] == "..":
                    if current_path.count("/") > 0:
                        current_path = current_path.rsplit("/", 1)[0]
                elif l.split()[2] == "/":
                    current_path = "/"
        else:
            if "dir" not in l:
                file_size[(current_path + "/" if len(current_path) >
                           1 else "/") + l.split()[1]] = int(l.split()[0])

    folder_size = defaultdict(int)
    for f in file_size:
        folder = Path(f).parent
        while True:
            folder_size[folder] += file_size[f]
            if folder == Path("/"):
                break
            folder = folder.parent

    
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
