use std::time;
use std::collections::HashMap;

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}

fn part_1() {
    let mut l1: Vec<i32> = Vec::new();
    let mut l2: Vec<i32> = Vec::new();

    for line in include_str!("input.txt").split("\n") {
        let parts: Vec<&str> = line.split_whitespace().collect();
        if parts.len() == 2 {
            let a: i32 = parts[0].parse().unwrap();
            let b: i32 = parts[1].parse().unwrap();
            l1.push(a);
            l2.push(b);
        }
    }

    l1.sort();
    l2.sort();

    let sum: i32 = l1.iter().zip(l2.iter())
        .map(|(a, b)| (a - b).abs())
        .sum();

    println!("{}", sum);
}

fn part_2() {
    let mut l1: Vec<i32> = Vec::new();
    let mut l2: Vec<i32> = Vec::new();

    for line in include_str!("input.txt").split("\n") {
        let parts: Vec<&str> = line.split_whitespace().collect();
        if parts.len() == 2 {
            let a: i32 = parts[0].parse().unwrap();
            let b: i32 = parts[1].parse().unwrap();
            l1.push(a);
            l2.push(b);
        }
    }

    let mut count_map: HashMap<i32, i32> = HashMap::new();
    for &value in &l2 {
        *count_map.entry(value).or_insert(0) += 1;
    }

    //let sum: i32 = l1.iter().map(|&l| l * count_map.get(&l).unwrap_or(&0)).sum();

    println!("{}", l1.iter().map(|&l| l * count_map.get(&l).unwrap_or(&0)).sum::<i32>());
}

fn main() {
    bench(part_1);
    bench(part_2);
}
