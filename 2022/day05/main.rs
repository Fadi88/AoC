use std::collections::HashMap;
use std::time;

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}

fn part_1() {
    let parts: Vec<_> = include_str!("input.txt").split("\n\n").collect();
    let config: Vec<_> = parts[0].lines().collect();

    let mut cargo: HashMap<char, Vec<char>> = HashMap::new();

    for l in &config {
        for (i, c) in l.chars().enumerate() {
            if c.is_alphabetic() {
                cargo
                    .entry(config.last().unwrap().as_bytes()[i] as char)
                    .or_insert(Vec::<char>::new())
                    .insert(0, c);
            }
        }
    }

    for l in parts[1].lines() {
        let mv = l
            .replace("from ", "")
            .replace("to ", "")
            .replace("move ", "");
        let idx: Vec<&str> = mv.split(" ").collect();

        let mut to_move = cargo
            .get(&idx[1].chars().last().unwrap())
            .unwrap()
            .iter()
            .rev()
            .take(idx[0].parse::<usize>().unwrap())
            .map(|x| x.clone())
            .collect::<Vec<_>>();

        let len = cargo.get(&idx[1].chars().last().unwrap()).unwrap().len();
        cargo
            .get_mut(&idx[1].chars().last().unwrap())
            .unwrap()
            .drain(len - idx[0].parse::<usize>().unwrap()..);

        cargo
            .get_mut(&idx[2].chars().last().unwrap())
            .unwrap()
            .append(&mut to_move);
    }

    for i in 1..10 {
        print!(
            "{}",
            cargo
                .get(&i.to_string().chars().last().unwrap())
                .unwrap()
                .last()
                .unwrap()
        );
    }

    println!("");
}

fn part_2() {
    let parts: Vec<_> = include_str!("input.txt").split("\n\n").collect();
    let config: Vec<_> = parts[0].lines().collect();

    let mut cargo: HashMap<char, Vec<char>> = HashMap::new();

    for l in &config {
        for (i, c) in l.chars().enumerate() {
            if c.is_alphabetic() {
                cargo
                    .entry(config.last().unwrap().as_bytes()[i] as char)
                    .or_insert(Vec::<char>::new())
                    .insert(0, c);
            }
        }
    }

    for l in parts[1].lines() {
        let mv = l
            .replace("from ", "")
            .replace("to ", "")
            .replace("move ", "");
        let idx: Vec<&str> = mv.split(" ").collect();

        let mut to_move = cargo
            .get(&idx[1].chars().last().unwrap())
            .unwrap()
            .iter()
            .rev()
            .take(idx[0].parse::<usize>().unwrap())
            .map(|x| x.clone())
            .rev()
            .collect::<Vec<_>>();

        let len = cargo.get(&idx[1].chars().last().unwrap()).unwrap().len();
        cargo
            .get_mut(&idx[1].chars().last().unwrap())
            .unwrap()
            .drain(len - idx[0].parse::<usize>().unwrap()..);

        cargo
            .get_mut(&idx[2].chars().last().unwrap())
            .unwrap()
            .append(&mut to_move);
    }

    for i in 1..10 {
        print!(
            "{}",
            cargo
                .get(&i.to_string().chars().last().unwrap())
                .unwrap()
                .last()
                .unwrap()
        );
    }

    println!("");
}

fn main() {
    bench(part_1);
    bench(part_2);
}
