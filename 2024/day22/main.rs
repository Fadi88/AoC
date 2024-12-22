use std::collections::{HashMap,HashSet};
use std::time::Instant;

fn bench<F, R>(f: F) -> R
where
    F: FnOnce() -> R,
{
    let t0 = Instant::now();
    let result = f(); // Call the function and store the result
    println!("time used: {:?}", Instant::now().duration_since(t0));
    result // Return the result of the function
}
fn gen_new(n: i64) -> i64 {
    let mut n = n;

    n ^= n * 64;
    n %= 16777216;

    n ^= n / 32 as i64;
    n %= 16777216;

    n ^= n * 2048;
    n %= 16777216;

    n
}

fn part_1() {
    let data: Vec<i64> = include_str!("input.txt")
        .lines()
        .map(|line| line.parse().expect("Not a number"))
        .collect();

    let mut data = data;
    for _ in 0..2000 {
        data = data.iter().map(|&n| gen_new(n)).collect();
    }

    println!("{}", data.iter().sum::<i64>());
}

fn get_deltas(n: i64) -> Vec<(i64, i64)> {
    let mut deltas = Vec::new();
    let mut n = n;

    for _ in 0..2000 {
        let new_n = gen_new(n);
        let b = n % 10;
        let nb = new_n % 10;
        deltas.push((nb - b, nb));
        n = new_n;
    }

    deltas
}

fn part_2() {
    let data: Vec<i64> = include_str!("input.txt")
        .lines()
        .map(|line| line.parse().expect("Not a number"))
        .collect();

    let mut patterns_roi: HashMap<(i64, i64, i64, i64), i64> = HashMap::new();

    for init in data {
        let deltas = get_deltas(init);
        let mut added = HashSet::new();
        for idx in 0..deltas.len() - 4 {
            let pat = (
                deltas[idx].0,
                deltas[idx + 1].0,
                deltas[idx + 2].0,
                deltas[idx + 3].0,
            );
            if !added.contains(&pat) {
                *patterns_roi.entry(pat).or_insert(0) += deltas[idx + 3].1;
                added.insert(pat);
            }
        }
    }

    println!("{}", patterns_roi.values().max().unwrap_or(&0));
}

fn main() {
    bench(part_1);
    bench(part_2);
}
