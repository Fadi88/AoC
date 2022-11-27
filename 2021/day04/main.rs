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

    let nums: Vec<_> = ls[0]
        .split(',')
        .map(|x| x.parse::<i16>().unwrap())
        .collect();

    let mut boards: Vec<Vec<Vec<i16>>> = Vec::new();

    for board in ls.iter().skip(1) {
        let mut b: Vec<Vec<i16>> = Vec::new();
        for l in board.split('\n') {
            b.push(
                l.split_whitespace()
                    .map(|n| n.parse::<i16>().unwrap())
                    .collect(),
            );
        }
        boards.push(b);
    }
    for num in nums{
        for board in &boards{
            for l in board{
                if l.contains(&num){
                    
                }
            }
        }
    }
}


fn part_2() {}

fn main() {
    bench(part_1);
    bench(part_2);
}
