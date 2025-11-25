import os
import time
import functools

# pylint: disable=fixme

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"[{func.__name__}] Result: {result}")
        print(f"[{func.__name__}] Time: {(end - start) * 1000:.4f}ms")
        return result
    return wrapper

def read_input():
    input_path = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(input_path, "r") as f:
        return f.read().strip()

@timer
def part_1(data: str) -> int:
    # TODO: Solve Part 1
    return len(data)

@timer
def part_2(data: str) -> int:
    # TODO: Solve Part 2
    return len(data)

def main():
    input_data = read_input()
    part_1(input_data)
    part_2(input_data)

if __name__ == "__main__":
    main()
