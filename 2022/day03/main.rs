use std::collections::HashSet;
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::time;

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}
fn get_value(c: char) -> u8 {
    if (c as u8) < ('a' as u8) {
        (c as u8) - ('A' as u8) + 1 + 26
    } else {
        (c as u8) - ('a' as u8) + 1
    }
}

fn part_1() {
    let input = BufReader::new(File::open("day03/input.txt").unwrap()).lines();

    let mut total: u16 = 0;
    for read_result in input {
        let l = read_result.unwrap();
        let h1: HashSet<char> = l[..l.len() / 2].chars().collect();
        let h2: HashSet<char> = l[l.len() / 2..].chars().collect();

        total += get_value(*h1.intersection(&h2).into_iter().last().unwrap()) as u16;
    }

    println!("{}", total);
}

fn part_2() {
    let input: Vec<&str> = include_str!("input.txt").split("\n").collect();
    let mut total: u16 = 0;
    for i in (0..input.len()).step_by(3) {
        let h1: HashSet<char> = input[i].chars().collect();
        let h2: HashSet<char> = input[i + 1].chars().collect();
        let h3: HashSet<char> = input[i + 2].chars().collect();

        let c = h1
            .intersection(&h2)
            .map(|x| x.clone())
            .collect::<HashSet<char>>()
            .intersection(&h3)
            .next()
            .unwrap()
            .clone();

        total += get_value(c) as u16;
    }

    println!("{}", total);
}

fn main() {
    bench(part_1);
    bench(part_2);
}
