use std::collections::{HashMap, HashSet, VecDeque};
use std::fs;
use std::time;

type GridType = HashSet<(i16, i16)>;

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}
fn is_isolated(grid: &GridType, e: &(i16, i16)) -> bool {
    for dy in [-1, 0, 1] {
        for dx in [-1, 0, 1] {
            if dx == 0 && dy == 0 {
                continue;
            }
            if grid.contains(&(e.0 + dx, e.1 + dy)) {
                return false;
            }
        }
    }
    true
}

fn part_1() {
    let mut grid: GridType = HashSet::new();
    for (y, l) in fs::read_to_string("input.txt")
        .unwrap()
        .lines()
        .into_iter()
        .enumerate()
    {
        for (x, c) in l.chars().enumerate() {
            if c == '#' {
                grid.insert((x as i16, y as i16));
            }
        }
    }

    let mut directions = VecDeque::from(["north", "south", "west", "east"]);
    let neighbors: HashMap<&str, Vec<(i16, i16)>> = [
        ("north", vec![(0, -1), (1, -1), (-1, -1)]),
        ("south", vec![(0, 1), (1, 1), (-1, 1)]),
        ("west", vec![(-1, 0), (-1, 1), (-1, -1)]),
        ("east", vec![(1, 0), (1, 1), (1, -1)]),
    ]
    .iter()
    .cloned()
    .collect();

    for _ in 0..10 {
        let mut proposal: HashMap<(i16, i16), (i16, i16)> = HashMap::new();
        let mut counts: HashMap<(i16, i16), u8> = HashMap::new();

        for e in grid.clone() {
            if is_isolated(&grid, &e) {
                continue;
            }

            for d in &directions {
                if neighbors
                    .get(d)
                    .unwrap()
                    .clone()
                    .iter()
                    .map(|delta| !grid.contains(&(e.0 + delta.0, e.1 + delta.1)))
                    .all(|x| x)
                {
                    let delta = neighbors.get(d).unwrap().get(0).unwrap();
                    proposal.insert(e.clone(), (e.0 + delta.0, e.1 + delta.1));
                    *counts.entry((e.0 + delta.0, e.1 + delta.1)).or_insert(0) += 1;
                    break;
                }
            }
        }
        let mut new_grid: GridType = HashSet::new();

        for e in grid {
            if proposal.contains_key(&e) && *counts.get(proposal.get(&e).unwrap()).unwrap() == 1 {
                new_grid.insert(proposal.get(&e).unwrap().clone());
            } else {
                new_grid.insert(e.clone());
            }
        }
        grid = new_grid;
        directions.rotate_left(1);
    }

    let xs = grid.iter().map(|p| p.0).collect::<HashSet<_>>();
    let ys = grid.iter().map(|p| p.1).collect::<HashSet<_>>();
    println!(
        "{}",
        (xs.iter().max().unwrap() - xs.iter().min().unwrap() + 1)
            * (ys.iter().max().unwrap() - ys.iter().min().unwrap() + 1)
            - grid.len() as i16
    );
}

fn part_2() {
    let mut grid: GridType = HashSet::new();
    for (y, l) in fs::read_to_string("input.txt")
        .unwrap()
        .lines()
        .into_iter()
        .enumerate()
    {
        for (x, c) in l.chars().enumerate() {
            if c == '#' {
                grid.insert((x as i16, y as i16));
            }
        }
    }

    let mut directions = VecDeque::from(["north", "south", "west", "east"]);
    let neighbors: HashMap<&str, Vec<(i16, i16)>> = [
        ("north", vec![(0, -1), (1, -1), (-1, -1)]),
        ("south", vec![(0, 1), (1, 1), (-1, 1)]),
        ("west", vec![(-1, 0), (-1, 1), (-1, -1)]),
        ("east", vec![(1, 0), (1, 1), (1, -1)]),
    ]
    .iter()
    .cloned()
    .collect();

    let mut cycle = 0;

    loop {
        let mut proposal: HashMap<(i16, i16), (i16, i16)> = HashMap::new();
        let mut counts: HashMap<(i16, i16), u8> = HashMap::new();

        for e in grid.clone() {
            if is_isolated(&grid, &e) {
                continue;
            }

            for d in &directions {
                if neighbors
                    .get(d)
                    .unwrap()
                    .clone()
                    .iter()
                    .map(|delta| !grid.contains(&(e.0 + delta.0, e.1 + delta.1)))
                    .all(|x| x)
                {
                    let delta = neighbors.get(d).unwrap().get(0).unwrap();
                    proposal.insert(e.clone(), (e.0 + delta.0, e.1 + delta.1));
                    *counts.entry((e.0 + delta.0, e.1 + delta.1)).or_insert(0) += 1;
                    break;
                }
            }
        }
        let mut new_grid: GridType = HashSet::new();

        for e in &grid {
            if proposal.contains_key(&e) && *counts.get(proposal.get(&e).unwrap()).unwrap() == 1 {
                new_grid.insert(proposal.get(&e).unwrap().clone());
            } else {
                new_grid.insert(e.clone());
            }
        }
        cycle += 1;
        if grid.eq(&new_grid){
            break
        }
        grid = new_grid;
        directions.rotate_left(1);
    }
    println!("{}" , cycle);
}

fn main() {
    bench(part_1);
    bench(part_2);
}
