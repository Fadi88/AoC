use std::time;

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}

fn part_1() {
    include_str!("input.txt");
}

fn part_2() {}

fn main() {
    bench(part_1);
    bench(part_2);
}
