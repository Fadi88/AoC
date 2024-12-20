use itertools::Itertools;
use std::collections::{BinaryHeap, HashMap, HashSet};
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

fn dijkstra(start: (i32, i32), free_spaces: &HashSet<(i32, i32)>) -> HashMap<(i32, i32), i32> {
    let mut to_visit = BinaryHeap::new();
    let mut visited = HashMap::new();
    visited.insert(start, 0);
    to_visit.push((0, start));

    while let Some((score, (cx, cy))) = to_visit.pop() {
        let score = -score; // Negate score due to BinaryHeap being a min-heap

        if visited.get(&(cx, cy)).map_or(false, |&v| v < score) {
            continue;
        }

        for (dx, dy) in [(0, 1), (0, -1), (1, 0), (-1, 0)] {
            let np = (cx + dx, cy + dy);
            if free_spaces.contains(&np) && visited.get(&np).map_or(true, |&v| v > score + 1) {
                visited.insert(np, score + 1);
                to_visit.push((-(score + 1), np));
            }
        }
    }

    visited
}

fn get_savings(distances: &HashMap<(i32, i32), i32>, jump_size: i32) -> usize {
    let mut ret = 0;
    for p in distances.keys() {
        for (dx, dy) in (-jump_size..=jump_size)
            .cartesian_product(-jump_size..=jump_size)
            .filter(|(dx, dy)| !(*dx == 0 && *dy == 0) && dx.abs() + dy.abs() <= jump_size)
        {
            let np = (p.0 + dx, p.1 + dy);
            if let Some(&initial_cost) = distances.get(p) {
                if let Some(&np_cost) = distances.get(&np) {
                    let cheat_cost = dx.abs() + dy.abs();
                    if (initial_cost - np_cost - cheat_cost) >= 100 {
                        ret += 1;
                    }
                }
            }
        }
    }
    ret
}

fn get_savings_2(distances: &HashMap<(i32, i32), i32>, jump_size: i32) -> usize {
    let mut ret = 0;

    let mut keys: Vec<_> = distances.keys().cloned().collect();
    keys.sort_by_key(|k| distances[k]);

    for i in 0..keys.len() {
        let p = keys[i];
        for j in (i + 1)..keys.len() {
            let np = keys[j];
            let cheat_cost = (p.0 - np.0).abs() + (p.1 - np.1).abs();
            let initial_cost = distances[&np] - distances[&p];
            if cheat_cost <= jump_size && (initial_cost - cheat_cost) >= 100 {
                ret += 1;
            }
        }
    }

    ret
}

fn part_1() {
    let input_file = include_str!("input.txt");
    let mut free_space = HashSet::new();
    let mut start = None;

    for (y, line) in input_file.lines().enumerate() {
        for (x, c) in line.chars().enumerate() {
            if c != '#' {
                free_space.insert((x as i32, y as i32));
            }
            if c == 'S' {
                start = Some((x as i32, y as i32));
            }
        }
    }

    let start = start.expect("No starting position found");
    let distances = dijkstra(start, &free_space);

    let savings = get_savings(
        &distances
            .iter()
            .map(|(&k, &v)| (k, v))
            .collect::<HashMap<(i32, i32), i32>>(),
        2,
    );

    println!("{}", savings);
}

fn part_2() {
    let input_file = include_str!("input.txt");
    let mut free_space = HashSet::new();
    let mut start = None;

    for (y, line) in input_file.lines().enumerate() {
        for (x, c) in line.chars().enumerate() {
            if c != '#' {
                free_space.insert((x as i32, y as i32));
            }
            if c == 'S' {
                start = Some((x as i32, y as i32));
            }
        }
    }

    let start = start.expect("No starting position found");
    let distances = dijkstra(start, &free_space);

    let savings = get_savings(
        &distances
            .iter()
            .map(|(&k, &v)| (k, v))
            .collect::<HashMap<(i32, i32), i32>>(),
        20,
    );

    println!("{}", savings);
}

fn main() {
    bench(part_1);
    bench(part_2);
}
