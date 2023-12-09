use std::collections::HashSet;
use std::time;

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}
fn get_next(l: Vec<i32>) -> i32 {
    let mut m: Vec<Vec<i32>> = Vec::new();
    m.push(l.clone());

    while HashSet::<i32>::from_iter(m.last().cloned().unwrap()).len() > 1 {
        let mut new_l: Vec<i32> = Vec::new();
        for i in 1..(m.last().unwrap().len()) {
            new_l.push(m.last().unwrap().get(i).unwrap() - m.last().unwrap().get(i - 1).unwrap());
        }
        m.push(new_l);
    }

    for i in (0..(&m.len() - 1)).rev() {
        let d = m.get(i + 1).unwrap().last().unwrap().clone();
        let last = m.get(i).unwrap().last().unwrap().clone();
        m.get_mut(i).unwrap().push(last + d);
    }

    m.first().unwrap().last().unwrap().clone()
}

fn part_1() {
    let next: i32 = include_str!("input.txt")
        .split("\n")
        .map(|l| {
            l.split(' ')
                .map(|c| c.parse::<i32>().unwrap())
                .collect::<Vec<_>>()
        })
        .map(get_next)
        .sum();

    dbg!(next);
}

fn part_2() {
    let prev: i32 = include_str!("input.txt")
        .split("\n")
        .map(|l| {
            l.split(' ')
                .map(|c| c.parse::<i32>().unwrap())
                .rev()
                .collect::<Vec<_>>()
        })
        .map(get_next)
        .sum();

    dbg!(prev);
}

fn main() {
    bench(part_1);
    bench(part_2);
}
