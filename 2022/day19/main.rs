use regex::Regex;
use std::collections::{HashMap, HashSet, VecDeque};
use std::fs;
use std::time;

type BluePrint = (u16, u16, u16, u16, u16, u16, u16);

#[derive(Eq, Hash, PartialEq, Clone, Debug)]
struct State {
    time: u16,

    ore: u16,
    ore_bot: u16,

    clay: u16,
    clay_bot: u16,

    obsidian: u16,
    obsidian_bot: u16,

    geode: u16,
    geode_bot: u16,
}

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}

impl Default for State {
    fn default() -> Self {
        Self {
            time: 0,
            ore: 0,
            ore_bot: 1,
            clay: 0,
            clay_bot: 0,
            obsidian: 0,
            obsidian_bot: 0,
            geode: 0,
            geode_bot: 0,
        }
    }
}

fn get_max_geode(blue_print: &BluePrint, limit: u16) -> u16 {
    let init_state = State {
        ..Default::default()
    };
    let mut possible_scores: Vec<u32> = Vec::new();

    let mut to_visit: VecDeque<State> = VecDeque::new();
    to_visit.push_back(init_state);

    let mut seen: HashSet<State> = HashSet::new();

    let mut best_geode: HashMap<u16, u16> = HashMap::new();

    while !to_visit.is_empty() {
        let mut current_state = to_visit.pop_front().unwrap();

        if seen.contains(&current_state) {
            continue;
        }

        seen.insert(current_state.clone());

        current_state.time += 1;

        if current_state.time > limit {
            possible_scores.push(blue_print.0 as u32 * current_state.geode as u32);
            continue;
        }

        let (mut n_cl, mut n_or, mut n_ob, mut n_ge) = (0, 0, 0, 0);

        if current_state.ore >= blue_print.1 {
            n_or += 1;
        }

        if current_state.ore >= blue_print.2 {
            n_cl += 1;
        }

        if current_state.ore >= blue_print.3 && current_state.clay >= blue_print.4 {
            n_ob = 1;
        }

        if current_state.ore >= blue_print.5 && current_state.obsidian >= blue_print.6 {
            n_ge = 1;
        }

        current_state.ore += current_state.ore_bot;
        current_state.clay += current_state.clay_bot;
        current_state.geode += current_state.geode_bot;
        current_state.obsidian += current_state.obsidian_bot;

        let delta = if limit != 24 && current_state.time > 21 {
            1
        } else {
            0
        };

        if current_state.geode + delta < *best_geode.entry(current_state.time).or_insert(0) {
            continue;
        } else if current_state.geode > *best_geode.entry(current_state.time).or_insert(0) {
            *best_geode.get_mut(&current_state.time).unwrap() = current_state.geode;
        }

        if n_ge == 1 {
            let mut new_state = current_state.clone();
            new_state.geode_bot += 1;
            new_state.ore -= blue_print.5;
            new_state.obsidian -= blue_print.6;

            to_visit.push_back(new_state);
            continue;
        }

        if n_ob == 1 && current_state.obsidian_bot < blue_print.6 {
            let mut new_state = current_state.clone();
            new_state.obsidian_bot += 1;
            new_state.ore -= blue_print.3;
            new_state.clay -= blue_print.4;

            to_visit.push_back(new_state);
        }

        if n_cl == 1 && current_state.clay_bot < blue_print.4 {
            let mut new_state = current_state.clone();
            new_state.clay_bot += 1;
            new_state.ore -= blue_print.2;

            to_visit.push_back(new_state);
        }

        if n_or == 1
            && current_state.ore_bot
                < *[blue_print.1, blue_print.2, blue_print.3, blue_print.5]
                    .iter()
                    .max()
                    .unwrap()
        {
            let mut new_state = current_state.clone();
            new_state.ore_bot += 1;
            new_state.ore -= blue_print.1;
            to_visit.push_back(new_state);
        }

        to_visit.push_back(current_state);
    }
    (*possible_scores.iter().max().unwrap()).try_into().unwrap()
}

fn part_1() {
    let re = Regex::new(r"(\d+)").unwrap();
    let mut blue_prints: Vec<BluePrint> = Vec::new();

    for l in fs::read_to_string("input.txt").unwrap().lines() {
        let p = re
            .find_iter(l)
            .map(|x| x.as_str().parse::<u16>().unwrap())
            .collect::<Vec<_>>();

        blue_prints.push((p[0], p[1], p[2], p[3], p[4], p[5], p[6]));
    }
    let l = blue_prints.iter().map(|x| get_max_geode(x, 24) as u32);
    println!("{}", l.sum::<u32>());
}

fn part_2() {
    let re = Regex::new(r"(\d+)").unwrap();
    let mut blue_prints: Vec<BluePrint> = Vec::new();

    for l in fs::read_to_string("input.txt").unwrap().lines() {
        let p = re
            .find_iter(l)
            .map(|x| x.as_str().parse::<u16>().unwrap())
            .collect::<Vec<_>>();

        blue_prints.push((p[0], p[1], p[2], p[3], p[4], p[5], p[6]));
    }
    println!(
        "{}",
        blue_prints
            .iter()
            .take(3)
            .map(|x| get_max_geode(x, 32))
            .reduce(|x, y| x * y)
            .unwrap()
            / blue_prints
                .iter()
                .take(3)
                .map(|x| x.0)
                .reduce(|x, y| x * y)
                .unwrap()
    );
}

fn main() {
    bench(part_1);
    bench(part_2);
}
