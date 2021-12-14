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

    let mut freq : HashMap<char,u16> = HashMap::new();

    for i in HashSet::<char>::from_iter(formula.chars()){
        freq.insert(i, formula.matches(i).count() as u16);
    }

    println!("{:?}" , freq.values().max().unwrap() - freq.values().min().unwrap() ) ;
}

fn part_2() {}

fn main() {
    bench(part_1);
    bench(part_2);
}
