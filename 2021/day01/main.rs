use std::fs;
use std::time;

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}

fn part_1() {
    let nums: Vec<u16> = fs::read_to_string("day01/input.txt")
        .unwrap()
        .lines()
        .map(|v| v.parse::<u16>().unwrap())
        .collect();

    let mut cnt: u16 = 0;
    for i in 1..nums.len() {
        if nums[i] > nums[i - 1] {
            cnt += 1;
        }
    }

    println!("part 1 : {}", cnt);
}

fn part_2() {
    let nums: Vec<u16> = fs::read_to_string("day01/input.txt")
        .unwrap()
        .lines()
        .map(|v| v.parse::<u16>().unwrap())
        .collect();

    let mut cnt: u16 = 0;
    for i in 2..nums.len() - 1 {
        if nums[i + 1] > nums[i - 2] {
            cnt += 1;
        }
    }

    println!("part 2 : {}", cnt);
}

fn main() {
    bench(part_1);
    bench(part_2);
}
