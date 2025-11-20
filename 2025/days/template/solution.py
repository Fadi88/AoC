import os
import time

def read_input():
    input_path = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(input_path, "r") as f:
        return f.read().strip()

def part_1(input_data):
    # TODO: Solve Part 1
    return len(input_data)

def part_2(input_data):
    # TODO: Solve Part 2
    return len(input_data)

def run_part(name, func, input_data):
    start = time.time()
    result = func(input_data)
    end = time.time()
    print(f"[{name}] Result: {result}")
    print(f"[{name}] Time: {(end - start) * 1000:.4f}ms")

if __name__ == "__main__":
    input_data = read_input()
    run_part("Part 1", part_1, input_data)
    run_part("Part 2", part_2, input_data)
