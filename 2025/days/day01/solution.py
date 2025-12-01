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
        duration = end - start
        time_units = {
            "us": (1e-3, 1e6),
            "ms": (1, 1e3),
            "s":  (float('inf'), 1),
        }
        for unit, (threshold, multiplier) in time_units.items():
            if duration < threshold:
                print(f"[{func.__name__}] Time: {duration * multiplier:.4f} {unit}")
                break
        return result
    return wrapper

def read_input():
    input_path = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(input_path, "r") as f:
        return f.read().strip().split()

@timer
def part_1(data: list[str]) -> int:
    p = 50
    zeros = 0
    
    for r in data:        
        if r[0] == 'R':
            p = (p + int(r[1:])) % 100
        elif r[0] == 'L':
            p = (p - int(r[1:])) % 100
            
        if p == 0:
            zeros += 1
    return zeros

@timer
def part_2(data: list[str]) -> int:
    p = 50
    zeros = 0
    
    for r in data:
        amt = int(r[1:])
        
        if r[0] == 'R':
            new_p = (p + amt) % 100
            zeros += amt // 100
            if new_p < p:
                zeros += 1
            p = new_p
        elif r[0] == 'L':
            new_p = (p - amt) % 100
            zeros += amt // 100
            if p != 0 and (new_p > p or new_p == 0):
                zeros += 1
            p = new_p
            
    return zeros

def main():
    input_data = read_input()
    part_1(input_data)
    part_2(input_data)

if __name__ == "__main__":
    main()
