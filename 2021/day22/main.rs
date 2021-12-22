use regex::Regex;
use std::cmp::{max, min};
use std::collections::HashSet;
use std::time;

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}

fn part_1() {
    let re = Regex::new(r".*=(-?\d+)\.+(-?\d+).*=(-?\d+)\.+(-?\d+).*=(-?\d+)\.+(-?\d+)").unwrap();
    let mut pts: HashSet<(i32, i32, i32)> = HashSet::new();

    for l in include_str!("input.txt").split("\n") {
        let t: Vec<_> = re
            .captures(l)
            .unwrap()
            .iter()
            .skip(1)
            .map(|x| x.unwrap().as_str().parse::<i32>().unwrap())
            .collect();

        if t[0] > 50 || t[1] < -50 || t[2] > 50 || t[3] < -50 || t[4] > 50 || t[5] < -50 {
            continue;
        }

        for x in max(t[0], -50)..min(50, t[1] + 1) {
            for y in max(t[2], -50)..min(50, t[3] + 1) {
                for z in max(t[4], -50)..min(50, t[5] + 1) {
                    if l.contains("on") {
                        pts.insert((x, y, z));
                    } else {
                        pts.remove(&(x, y, z));
                    }
                }
            }
        }
    }
    println!("{}" , pts.len());
}

fn part_2() {}

fn main() {
    bench(part_1);
    bench(part_2);
}
