use std::fs::*;
use std::io::Read;
use std::time;

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}

fn part_1() {
    let mut buf = String::new();
    File::open("day04/input.txt")
        .unwrap()
        .read_to_string(&mut buf)
        .unwrap();

    let ls: Vec<_> = buf.split("\n\n").collect();

    let _nums: Vec<_> = ls[0]
        .split(',')
        .map(|x| x.parse::<u16>().unwrap())
        .collect();

    //println!("{}", ls[1]);
    let mut _baords = ls
        .iter()
        .skip(1)
        .map(|b_st| b_st.split('\n').collect::<Vec<_>>())
        .collect::<Vec<_>>()
        .iter()
        .map(|s| s.split("\n").collect::<Vec<_>>());
}

fn part_2() {}

fn main() {
    bench(part_1);
    bench(part_2);
}
