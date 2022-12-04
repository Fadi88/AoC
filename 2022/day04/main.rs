use regex::Regex;
use std::time;

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}

fn is_fully_contained(re: &Regex, s: &str) -> bool {
    let ds = re
        .captures_iter(s)
        .map(|x| x.get(0).unwrap().as_str().parse::<u8>().unwrap())
        .collect::<Vec<u8>>();
    if (ds[0] <= ds[2] && ds[1] >= ds[3]) || (ds[2] <= ds[0] && ds[3] >= ds[1]) {
        true
    } else {
        false
    }
}

fn part_1() {
    let re = Regex::new(r"\d+").unwrap();

    println!(
        "{}",
        include_str!("input.txt")
            .split("\n")
            .filter(|x| is_fully_contained(&re, x))
            .count()
    );
}

fn is_overlapping(re: &Regex, s: &str) -> bool {
    let ds = re
        .captures_iter(s)
        .map(|x| x.get(0).unwrap().as_str().parse::<u8>().unwrap())
        .collect::<Vec<u8>>();
    if (ds[2] >= ds[0] && ds[2] <= ds[1])
        || (ds[3] >= ds[0] && ds[3] <= ds[1])
        || (ds[0] >= ds[2] && ds[0] <= ds[3])
        || (ds[1] >= ds[2] && ds[1] <= ds[3])
    {
        true
    } else {
        false
    }
}

fn part_2() {
    let re = Regex::new(r"\d+").unwrap();

    println!(
        "{}",
        include_str!("input.txt")
            .split("\n")
            .filter(|x| is_overlapping(&re, x))
            .count()
    );
}

fn main() {
    bench(part_1);
    bench(part_2);
}
