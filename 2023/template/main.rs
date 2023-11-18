use std::time;
use std::fs;

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}

fn part_1() {
    fs::read_to_string("template/input.txt").unwrap().split("\n");
}

fn part_2() {
    fs::read_to_string("template/input.txt").unwrap().split("\n");
}

fn main() {
    bench(part_1);
    bench(part_2);
}
