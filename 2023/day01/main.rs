use std::collections::HashMap;
use std::fs;
use std::time;

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}

fn part_1() {
    let mut total = 0u32;
    for l in fs::read_to_string("day01/input.txt").unwrap().split("\n") {
        let digits: Vec<_> = l.chars().filter_map(|a| a.to_digit(10)).collect();

        total += digits.get(0).unwrap() * 10u32 + digits.get(digits.len() - 1).unwrap();
    }
    dbg!(total);
}

fn part_2() {
    let mut total = 0u32;

    let vals: HashMap<&str, char> = [
        ("one", '1'),
        ("two", '2'),
        ("three", '3'),
        ("four", '4'),
        ("five", '5'),
        ("six", '6'),
        ("seven", '7'),
        ("eight", '8'),
        ("nine", '9'),
        ("zero", '0'),
    ]
    .iter()
    .cloned()
    .collect();

    for l in fs::read_to_string("day01/input.txt").unwrap().split("\n") {
        let mut line = l.to_owned();
        let mut digits = Vec::<char>::new();
        while line.len() > 0 {
            if line.chars().nth(0).unwrap().is_digit(10) {
                digits.push(line.chars().nth(0).unwrap());
            } else {
                for d in vals.keys() {
                    if line.starts_with(d) {
                        digits.push(vals.get(d).unwrap().clone());
                        break;
                    }
                }
            }
            line.remove(0);
        }
        total += digits.get(0).unwrap().to_digit(10).unwrap() * 10u32
            + digits.get(digits.len() - 1).unwrap().to_digit(10).unwrap();
    }
    dbg!(total);
}

fn main() {
    bench(part_1);
    bench(part_2);
}
