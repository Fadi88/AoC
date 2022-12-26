use regex::Regex;
use std::collections::{HashMap, HashSet, VecDeque};
use std::fs;
use std::time;

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}
fn explore<'a>(
    grid: &'a HashMap<&'a str, Vec<&'a str>>,
    key_valves: &'a Vec<&'a str>,
    v: &'a str,
) -> HashMap<&'a str, u8> {
    let mut ret: HashMap<&str, u8> = HashMap::new();

    for target_v in key_valves {
        if target_v == &v {
            continue;
        }

        let mut to_visit: VecDeque<Vec<&str>> = VecDeque::new();
        to_visit.push_back(vec![v]);

        while !to_visit.is_empty() {
            let current_path = to_visit.pop_front().unwrap();

            if target_v == current_path.last().unwrap() {
                ret.insert(target_v, (current_path.len() - 1) as u8);
                break;
            }

            for n_v in grid.get(current_path.last().unwrap()).unwrap() {
                if current_path.contains(&n_v) {
                    continue;
                }

                let mut new_path = current_path.clone();
                new_path.push(n_v);

                to_visit.push_back(new_path);
            }
        }
    }

    ret
}

fn get_time_elapsed(grid: &HashMap<&str, HashMap<&str, u8>>, path: &Vec<&str>) -> u16 {
    let mut time_elapsed = 0;

    for i in 1..path.len() {
        time_elapsed += *grid.get(path[i - 1]).unwrap().get(path[i]).unwrap() as u16 + 1;
    }
    time_elapsed
}

fn get_pressure(
    grid: &HashMap<&str, HashMap<&str, u8>>,
    flow_rate: &HashMap<&str, u8>,
    path: &Vec<&str>,
    time: u16,
) -> u16 {
    let mut total_pressure = 0;
    let mut time_remaining = time;

    for i in 1..path.len() {
        let t = *grid.get(path[i - 1]).unwrap().get(path[i]).unwrap() as u16;
        if time_remaining > t + 1 {
            time_remaining -= t + 1;
            total_pressure += (*flow_rate.get(path[i]).unwrap() as u16) * time_remaining;
        } else {
            break;
        }
    }
    total_pressure
}

fn part_1() {
    let mut grid: HashMap<&str, Vec<&str>> = HashMap::new();
    let mut flow_rate: HashMap<&str, u8> = HashMap::new();

    let binding = fs::read_to_string("input.txt").unwrap();
    for l in binding.lines() {
        let re1 = Regex::new(r"\d+").unwrap();
        let re2 = Regex::new(r"[A-Z]{2}").unwrap();

        let p = re2.find_iter(l).map(|x| x.as_str()).collect::<Vec<_>>();

        grid.insert(
            p[0],
            p[1..].iter().map(|x| *x).collect(),
        );

        let flow = re1.find(l).unwrap().as_str().parse::<u8>().unwrap();

        if flow > 0 {
            flow_rate.insert(p[0], flow);
        }
    }

    let mut key_valves = flow_rate.keys().map(|y| *y).collect::<Vec<&str>>();
    key_valves.insert(0, "AA");

    let mut reduced_grid: HashMap<&str, HashMap<&str, u8>> = HashMap::new();

    for v in &key_valves {
        reduced_grid.insert(v.clone(), explore(&grid, &key_valves, v));
    }

    let mut to_visit: VecDeque<Vec<&str>> = VecDeque::new();
    to_visit.push_back(vec!["AA"]);

    let mut pressure: HashSet<u16> = HashSet::new();

    while !to_visit.is_empty() {
        let current_path = to_visit.pop_front().unwrap();

        if get_time_elapsed(&reduced_grid, &current_path) > 30
            || current_path.len() == key_valves.len()
        {
            pressure.insert(get_pressure(&reduced_grid, &flow_rate, &current_path, 30));
            continue;
        }

        for v in &key_valves {
            if !current_path.contains(v) {
                let mut new_path = current_path.clone();
                new_path.push(v);

                to_visit.push_back(new_path);
            }
        }
    }
    println!("{}", pressure.iter().max().unwrap());
}

fn part_2() {
    fs::read_to_string("input.txt").unwrap().split("\n");
}

fn main() {
    bench(part_1);
    bench(part_2);
}
