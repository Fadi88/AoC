use std::collections::{HashMap, HashSet};
use std::time;

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}

fn part_1() {
    let mut input = include_str!("input.txt").split("\n\n");

    let mut formula = String::from(input.next().unwrap());

    let mut trans: HashMap<String, char> = HashMap::new();

    for l in input.next().unwrap().split("\n") {
        let mut tmp = l.split(" -> ");
        trans.insert(
            String::from(tmp.next().unwrap()),
            tmp.next().unwrap().chars().next().unwrap(),
        );
    }

    for _ in 0..10 {
        let mut new_forumla: String = String::new();

        for i in 0..formula.len() - 1 {
            let c1 = formula.as_bytes()[i] as char;
            let c2 = formula.as_bytes()[i + 1] as char;
            new_forumla.push(c1);
            new_forumla.push(trans[&String::from_iter([c1, c2])]);
        }

        new_forumla.push(formula.as_bytes()[formula.len() - 1] as char);

        formula = new_forumla;
    }

    let mut freq: HashMap<char, u16> = HashMap::new();

    for i in HashSet::<char>::from_iter(formula.chars()) {
        freq.insert(i, formula.matches(i).count() as u16);
    }

    println!(
        "part 1 : {:?}",
        freq.values().max().unwrap() - freq.values().min().unwrap()
    );
}

fn part_2() {
    let mut input = include_str!("input.txt").split("\n\n");

    let formula = String::from(input.next().unwrap());

    let mut trans: HashMap<String, char> = HashMap::new();

    for l in input.next().unwrap().split("\n") {
        let mut tmp = l.split(" -> ");
        trans.insert(
            String::from(tmp.next().unwrap()),
            tmp.next().unwrap().chars().next().unwrap(),
        );
    }

    let mut pairs: HashMap<String, u64> = HashMap::new();
    for i in 0..formula.len() - 1 {
        *pairs
            .entry(formula.chars().skip(i).take(2).collect::<String>())
            .or_insert(0) += 1;
    }

    for _ in 0..40 {
        let mut new_pairs: HashMap<String, u64> = HashMap::new();

        for i in &pairs {
            let mut k1: String = String::new();
            let mut k2: String = String::new();
            k1.push(i.0.chars().nth(0).unwrap());
            k1.push(trans[i.0]);
            k2.push(trans[i.0]);
            k2.push(i.0.chars().nth(1).unwrap());

            *new_pairs.entry(k1).or_insert(0) += *i.1;
            *new_pairs.entry(k2).or_insert(0) += *i.1;
        }

        pairs = new_pairs;
    }

    let mut freq: HashMap<char, u64> = HashMap::new();

    for p in &pairs {
        *freq.entry(p.0.chars().nth(0).unwrap()).or_insert(0) += p.1;
        *freq.entry(p.0.chars().nth(1).unwrap()).or_insert(0) += p.1;
    }

    *freq.entry(formula.chars().nth(0).unwrap()).or_insert(0) += 1;
    *freq
        .entry(formula.chars().nth_back(0).unwrap())
        .or_insert(0) += 1;

    println!(
        "{:?}",
        (freq.values().max().unwrap() - freq.values().min().unwrap()) / 2
    );
}

fn main() {
    bench(part_1);
    bench(part_2);
}
