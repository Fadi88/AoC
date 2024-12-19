use std::collections::{HashMap, HashSet};
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

fn count_allowed(
    towel: &str,
    patterns: &HashSet<&str>,
    cache: &mut HashMap<String, usize>,
) -> usize {
    if let Some(&result) = cache.get(towel) {
        return result;
    }

    let mut combs = 0;
    for &p in patterns {
        if towel == p {
            combs += 1;
        }
        if towel.starts_with(p) {
            let new_towel = towel.replacen(p, "", 1);
            combs += count_allowed(&new_towel, patterns, cache);
        }
    }

    cache.insert(towel.to_string(), combs);
    combs
}

fn part_1() {
    let input_file = include_str!("input.txt");
    let ps: Vec<&str> = input_file.split("\n\n").collect();

    let allowed: HashSet<&str> = ps[0].split(", ").collect();
    let towels: Vec<&str> = ps[1].split_whitespace().collect();

    let mut cache = HashMap::new();
    let count = towels
        .iter()
        .filter(|&t| count_allowed(t, &allowed, &mut cache) > 0)
        .count();

    println!("{}", count);
}

fn part_2() {
    let input_file = include_str!("input.txt");
    let ps: Vec<&str> = input_file.split("\n\n").collect();

    let allowed: HashSet<&str> = ps[0].split(", ").collect();
    let towels: Vec<&str> = ps[1].split_whitespace().collect();

    let mut cache = HashMap::new();
    let total : u64= towels
        .iter()
        .map(|&t| count_allowed(t, &allowed, &mut cache) as u64)
        .sum();

    println!("{}", total);
}

fn main() {
    bench(part_1);
    bench(part_2);
}
