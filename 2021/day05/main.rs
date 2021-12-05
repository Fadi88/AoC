use std::cmp::{max, min};
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
    let mut cnt: HashMap<(u16, u16), u8> = HashMap::new();
    for l in fs::read_to_string("day05/input.txt").unwrap().lines() {
        let v: Vec<Vec<_>> = l
            .split(" -> ")
            .map(|x| x.split(',').map(|x| x.parse::<u16>().unwrap()).collect())
            .collect();
        let p1 = &v[0];
        let p2 = &v[1];

        if p1[0] == p2[0] {
            for i in min(p1[1], p2[1])..=max(p1[1], p2[1]) {
                *cnt.entry((p1[0], i)).or_insert(0) += 1;
            }
        } else if p1[1] == p2[1] {
            for i in min(p1[0], p2[0])..=max(p1[0], p2[0]) {
                *cnt.entry((i, p1[1])).or_insert(0) += 1;
            }
        }
    }

    println!("part 1 : {:?} ", cnt.values().filter(|x| **x > 1).count());
}

fn part_2() {
    let mut cnt: HashMap<(u16, u16), u8> = HashMap::new();
    for l in fs::read_to_string("day05/input.txt").unwrap().lines() {
        let v: Vec<Vec<_>> = l
            .split(" -> ")
            .map(|x| x.split(',').map(|x| x.parse::<u16>().unwrap()).collect())
            .collect();
        let p1 = &v[0];
        let p2 = &v[1];

        if p1[0] == p2[0] {
            for i in min(p1[1], p2[1])..=max(p1[1], p2[1]) {
                *cnt.entry((p1[0], i)).or_insert(0) += 1;
            }
        } else if p1[1] == p2[1] {
            for i in min(p1[0], p2[0])..=max(p1[0], p2[0]) {
                *cnt.entry((i, p1[1])).or_insert(0) += 1;
            }
        } else {
            let xs: Vec<u16>;
            let ys: Vec<u16>;
            if p1[0] < p2[0] {
                xs = (p1[0]..=p2[0]).collect();
            } else {
                xs = (p2[0]..=p1[0]).rev().collect();
            }

            if p1[1] < p2[1] {
                ys = (p1[1]..=p2[1]).collect();
            } else {
                ys = (p2[1]..=p1[1]).rev().collect();
            }

            for i in 0..ys.len() {
                *cnt.entry((xs[i], ys[i])).or_insert(0) += 1;
            }
        }
    }

    println!("part 2 : {:?} ", cnt.values().filter(|x| **x > 1).count());
}

fn main() {
    bench(part_1);
    bench(part_2);
}
