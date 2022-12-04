use std::time;

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}

fn is_fully_contained(s: &str) -> bool {
    let ds: Vec<_> = s
        .replace("-", ",")
        .split(',')
        .map(|x| x.parse::<u8>().unwrap())
        .collect();
    if (ds[0] <= ds[2] && ds[1] >= ds[3]) || (ds[2] <= ds[0] && ds[3] >= ds[1]) {
        true
    } else {
        false
    }
}

fn part_1() {
    println!(
        "{}",
        include_str!("input.txt")
            .lines()
            .filter(|x| is_fully_contained(x))
            .count()
    );
}

fn is_overlapping(s: &str) -> bool {
    let ds: Vec<_> = s
        .replace("-", ",")
        .split(',')
        .map(|x| x.parse::<u8>().unwrap())
        .collect();
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
    println!(
        "{}",
        include_str!("input.txt")
            .lines()
            .filter(|x| is_overlapping(x))
            .count()
    );
}

fn main() {
    bench(part_1);
    bench(part_2);
}
