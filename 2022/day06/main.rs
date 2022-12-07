use std::collections::HashSet;
use std::time;

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}

fn part_1() {
    let l = include_str!("input.txt").chars().collect::<Vec<_>>();

    let target_len = 4;

    for i in target_len..l.len() {
        let message: HashSet<&char> = HashSet::from_iter(l[(i - target_len)..i].iter());

        if message.len() == target_len {
            println!("{}", i);
            break;
        }
    }
}

fn part_2() {
    let l = include_str!("input.txt").chars().collect::<Vec<_>>();

    let target_len = 14;

    for i in target_len..l.len() {
        let message: HashSet<&char> = HashSet::from_iter(l[(i - target_len)..i].iter());

        if message.len() == target_len {
            println!("{}", i);
            break;
        }
    }
}

fn main() {
    bench(part_1);
    bench(part_2);
}
