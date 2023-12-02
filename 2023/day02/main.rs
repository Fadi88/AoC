use regex::Regex;
use std::fs;
use std::time;

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}

fn part_1() {
    let red_reg = Regex::new(r"(\d+) red").unwrap();
    let grn_reg = Regex::new(r"(\d+) green").unwrap();
    let blu_reg = Regex::new(r"(\d+) blue").unwrap();

    let id_reg = Regex::new(r"Game (\d+)").unwrap();

    let mut total = 0u16;

    for l in fs::read_to_string("day02/input.txt").unwrap().split("\n") {
        let red_cnt = red_reg
            .find_iter(l)
            .map(|d| {
                d.as_str()
                    .split(' ')
                    .filter_map(|d| d.parse::<u16>().ok())
                    .next()
                    .unwrap()
            })
            .max()
            .unwrap();

        let blu_cnt = blu_reg
            .find_iter(l)
            .map(|d| {
                d.as_str()
                    .split(' ')
                    .filter_map(|d| d.parse::<u16>().ok())
                    .next()
                    .unwrap()
            })
            .max()
            .unwrap();

        let grn_cnt = grn_reg
            .find_iter(l)
            .map(|d| {
                d.as_str()
                    .split(' ')
                    .filter_map(|d| d.parse::<u16>().ok())
                    .next()
                    .unwrap()
            })
            .max()
            .unwrap();

        let id = id_reg
            .captures(l)
            .unwrap()
            .get(1)
            .unwrap()
            .as_str()
            .parse::<u16>()
            .unwrap();

        if red_cnt <= 12 && grn_cnt <= 13 && blu_cnt <= 14 {
            total += id;
        }
    }
    dbg!(total);
}

fn part_2() {
    let red_reg = Regex::new(r"(\d+) red").unwrap();
    let grn_reg = Regex::new(r"(\d+) green").unwrap();
    let blu_reg = Regex::new(r"(\d+) blue").unwrap();

    let mut total = 0u16;

    for l in fs::read_to_string("day02/input.txt").unwrap().split("\n") {
        let red_cnt = red_reg
            .find_iter(l)
            .map(|d| {
                d.as_str()
                    .split(' ')
                    .filter_map(|d| d.parse::<u16>().ok())
                    .next()
                    .unwrap()
            })
            .max()
            .unwrap();

        let blu_cnt = blu_reg
            .find_iter(l)
            .map(|d| {
                d.as_str()
                    .split(' ')
                    .filter_map(|d| d.parse::<u16>().ok())
                    .next()
                    .unwrap()
            })
            .max()
            .unwrap();

        let grn_cnt = grn_reg
            .find_iter(l)
            .map(|d| {
                d.as_str()
                    .split(' ')
                    .filter_map(|d| d.parse::<u16>().ok())
                    .next()
                    .unwrap()
            })
            .max()
            .unwrap();

        total += red_cnt * blu_cnt * grn_cnt;
    }

    dbg!(total);
}

fn main() {
    bench(part_1);
    bench(part_2);
}
