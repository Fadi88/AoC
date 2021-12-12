use std::collections::{HashMap, VecDeque};
use std::time;

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}

fn part_1() {
    let mut grid: HashMap<&str, Vec<&str>> = HashMap::new();
    for l in include_str!("input.txt").split("\n") {
        let p: Vec<&str> = l.split("-").collect();
        grid.entry(p[0]).or_insert(Vec::new()).push(p[1]);
        grid.entry(p[1]).or_insert(Vec::new()).push(p[0]);
    }

    let mut to_visit: VecDeque<Vec<&str>> = VecDeque::new();
    let mut cnt = 0;

    for i in &grid["start"] {
        to_visit.push_back(vec!["start", &i]);
    }

    while to_visit.len() > 0 {
        let current_path = to_visit.pop_front().unwrap();
        if *current_path.last().unwrap() == "end" {
            cnt += 1;
            continue;
        }

        for i in &grid[current_path[current_path.len() - 1]] {
            if !(i.chars().all(|x| x.is_lowercase()) && current_path.contains(i)) {
                let mut tmp = current_path.clone();
                tmp.push(i);
                to_visit.push_back(tmp);
            }
        }
    }

    println!("part 1 : {}", cnt);
}
fn lower_pattern(path: &Vec<&str>) -> bool {
    let mut cnt: HashMap<&str, u16> = HashMap::new();

    for i in path.iter().skip(1) {
        if i.chars().all(|x| x.is_lowercase()) {
            *cnt.entry(i).or_insert(0) += 1;
        }
    }

    cnt.values().filter(|&&x| x > 2).count() == 0 && cnt.values().filter(|&&x| x == 2).count() < 2
}

fn part_2() {
    let mut grid: HashMap<&str, Vec<&str>> = HashMap::new();
    for l in include_str!("input.txt").split("\n") {
        let p: Vec<&str> = l.split("-").collect();
        grid.entry(p[0]).or_insert(Vec::new()).push(p[1]);
        grid.entry(p[1]).or_insert(Vec::new()).push(p[0]);
    }

    let mut to_visit: VecDeque<Vec<&str>> = VecDeque::new();
    let mut cnt = 0;

    for i in &grid["start"] {
        to_visit.push_back(vec!["start", &i]);
    }

    while to_visit.len() > 0 {
        let current_path = to_visit.pop_front().unwrap();
        if *current_path.last().unwrap() == "end" {
            cnt += 1;
            continue;
        }

        for i in &grid[current_path[current_path.len() - 1]] {
            if i == &"start" {
                continue;
            }

            let mut tmp = current_path.clone();
            tmp.push(i);
            if lower_pattern(&tmp) {
                to_visit.push_back(tmp);
            }
        }
    }

    println!("part 2 : {}", cnt);
}

fn main() {
    bench(part_1);
    bench(part_2);
}
