use std::time;

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}

fn part_1() {
    for l in include_str!("input.txt").split("\n\n"){

    }

}

fn part_2() {
    for l in include_str!("input.txt").split("\n\n"){

    }

}

fn main() {
    bench(part_1);
    bench(part_2);
}
