use std::collections::{HashMap, HashSet};
use std::time;

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}

fn part_1() {
    let input = include_str!("input.txt");
    let mut parts = input.split("\n\n");
    let order_lines = parts.next().unwrap();
    let sets_lines = parts.next().unwrap();

    let mut order: HashMap<i32, HashSet<i32>> = HashMap::new();
    for line in order_lines.lines() {
        let parts: Vec<&str> = line.split('|').collect();
        let from: i32 = parts[0].parse().unwrap();
        let to: i32 = parts[1].parse().unwrap();
        order.entry(from).or_default().insert(to);
    }

    let mut s = 0;
    for line in sets_lines.lines() {
        let update: Vec<i32> = line.split(',').map(|x| x.parse().unwrap()).collect();
        let mut ordered = true;
        for (i, &page) in update.iter().enumerate() {
            if !update[i + 1..]
                .iter()
                .all(|&page2| order.get(&page).map_or(false, |set| set.contains(&page2)))
            {
                ordered = false;
                break;
            }
        }
        if ordered {
            s += update[update.len() / 2];
        }
    }

    println!("{}", s);
}

fn part_2() {
    let input = include_str!("input.txt");
    let mut parts = input.split("\n\n");
    let order_lines = parts.next().unwrap();
    let sets_lines = parts.next().unwrap();

    let mut order: HashMap<i32, HashSet<i32>> = HashMap::new();
    for line in order_lines.lines() {
        let parts: Vec<&str> = line.split('|').collect();
        let from: i32 = parts[0].parse().unwrap();
        let to: i32 = parts[1].parse().unwrap();
        order.entry(from).or_default().insert(to);
    }

    let mut s = 0;
    for line in sets_lines.lines() {
        let update: Vec<i32> = line.split(',').map(|x| x.parse().unwrap()).collect();

        if update.iter().enumerate().all(|(i, &page)| {
            update[i + 1..]
                .iter()
                .all(|&page2| order.get(&page).map_or(false, |set| set.contains(&page2)))
        }) {
            continue;
        }

        let mut new_list = Vec::new();
        let mut to_sort: HashSet<i32> = update.iter().cloned().collect();

        while !to_sort.is_empty() {
            for &n in &to_sort {
                if to_sort
                    .iter()
                    .all(|&n2| n == n2 || order.get(&n).map_or(false, |set| set.contains(&n2)))
                {
                    new_list.push(n);
                    to_sort.remove(&n);
                    break;
                }
            }
        }

        s += new_list[new_list.len() / 2];
    }

    println!("{}", s);
}

fn main() {
    bench(part_1);
    bench(part_2);
}
