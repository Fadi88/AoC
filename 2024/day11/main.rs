use std::collections::HashMap;
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

fn count_after_blinking(l_cnt: Vec<u64>, n: u64) -> u64 {
    let mut l_cnt: HashMap<u64, u64> = l_cnt.into_iter().fold(HashMap::new(), |mut acc, x| {
        *acc.entry(x).or_insert(0) += 1;
        acc
    });

    for _ in 0..n {
        let mut new_l: HashMap<u64, u64> = HashMap::new();
        for (&s, &count) in &l_cnt {
            if s == 0 {
                *new_l.entry(1).or_insert(0) += count;
            } else if s.to_string().len() % 2 == 0 {
                let num_str = s.to_string();
                let mid = num_str.len() / 2;
                let n1 = num_str[..mid].parse::<u64>().unwrap();
                let n2 = num_str[mid..].parse::<u64>().unwrap();
                *new_l.entry(n1).or_insert(0) += count;
                *new_l.entry(n2).or_insert(0) += count;
            } else {
                *new_l.entry(s * 2024).or_insert(0) += count;
            }
        }
        l_cnt = new_l;
    }

    l_cnt.values().sum()
}

fn part_1() {
    let contents = include_str!("input.txt");
    let l: Vec<u64> = contents
        .split_whitespace()
        .map(|s| s.parse().unwrap())
        .collect();

    println!("{}", count_after_blinking(l, 25));
}

fn part_2() {
    let contents = include_str!("input.txt");
    let l: Vec<u64> = contents
        .split_whitespace()
        .map(|s| s.parse().unwrap())
        .collect();

    println!("{}", count_after_blinking(l, 75));
}

fn main() {
    bench(part_1);
    bench(part_2);
}
