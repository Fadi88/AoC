use std::time;

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}

fn is_safe(l: &Vec<i32>) -> bool {
    let mut sorted_asc = l.clone();
    sorted_asc.sort();

    let mut sorted_desc = sorted_asc.clone();
    sorted_desc.reverse();

    if l != &sorted_asc && l != &sorted_desc {
        return false;
    }

    for i in 1..l.len() {
        if (l[i] - l[i - 1]).abs() > 3 || (l[i] - l[i - 1]).abs() < 1 {
            return false;
        }
    }

    true
}

fn part_1() {
    let input = include_str!("input.txt");

    let reports: Vec<Vec<i32>> = input
        .lines()
        .map(|line| {
            line.split_whitespace()
                .map(|num| num.parse::<i32>().expect("Invalid number"))
                .collect()
        })
        .collect();
    println!("{}", reports.iter().filter(|line| is_safe(line)).count());
}

fn is_safe_tolerate(l: &Vec<i32>) -> bool {
    for i in 0..l.len() {
        let mut modified = l.clone();
        modified.remove(i);
        if is_safe(&modified) {
            return true;
        }
    }
    false
}
fn part_2() {
    let input = include_str!("input.txt");

    let reports: Vec<Vec<i32>> = input
        .lines()
        .map(|line| {
            line.split_whitespace()
                .map(|num| num.parse::<i32>().expect("Invalid number"))
                .collect()
        })
        .collect();
    println!("{}", reports.iter().filter(|line| is_safe_tolerate(line)).count());
}

fn main() {
    bench(part_1);
    bench(part_2);
}
