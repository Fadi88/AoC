use regex::Regex;
use std::time;

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}
fn get_sum(input: &str) -> i32 {
    let re = Regex::new(r"mul\((\d+),(\d+)\)").unwrap();
    re.captures_iter(input)
        .map(|cap| {
            let num1 = cap[1].parse::<i32>().unwrap();
            let num2 = cap[2].parse::<i32>().unwrap();
            num1 * num2
        })
        .sum()
}

fn part_1() {
    println!("{}", get_sum(include_str!("input.txt")));
}

fn part_2() {
    let re = Regex::new(r"don't\(\)[\s\S]*?do\(\)").unwrap();
    let input = re.replace_all(include_str!("input.txt"), "");
    println!("{}", get_sum(&input));
}

fn main() {
    bench(part_1);
    bench(part_2);
}
