use std::collections::{HashMap, VecDeque};
use std::fs;
use std::time;

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}

fn get_dist(grid: &HashMap<(i16, i16), char>, start: (i16, i16), end: (i16, i16)) -> Option<u16> {
    let mut visited: HashMap<(i16, i16), u16> = HashMap::new();
    let mut to_visit: VecDeque<(i16, i16)> = VecDeque::new();

    visited.insert(start, 0);
    to_visit.push_back(start);

    while !to_visit.is_empty() {
        let (cx, cy) = to_visit.pop_front().unwrap();

        for (dx, dy) in [(0, 1), (0, -1), (1, 0), (-1, 0)] {
            let (nx, ny) = ((cx + dx), (cy + dy));
            if grid.contains_key(&(nx, ny)) && !visited.contains_key(&(nx, ny)) {
                if *grid.get(&(nx, ny)).unwrap() as i16 - *grid.get(&(cx, cy)).unwrap() as i16 <= 1
                {
                    to_visit.push_back((nx, ny));
                    visited.insert((nx, ny), visited.get(&(cx, cy)).unwrap() + 1);

                    if (nx, ny) == end {
                        return Some(visited.get(&(cx, cy)).unwrap() + 1);
                    }
                }
            }
        }
    }
    None
}

fn part_1() {
    let mut grid: HashMap<(i16, i16), char> = HashMap::new();
    let mut start: (i16, i16) = (255, 255);
    let mut end: (i16, i16) = (255, 255);

    for (y, l) in fs::read_to_string("input.txt")
        .unwrap()
        .split("\n")
        .enumerate()
    {
        for (x, c) in l.chars().enumerate() {
            let mut height = c;
            if c.eq(&'S') {
                start = (x as i16, y as i16);
                height = 'a';
            } else if c.eq(&'E') {
                end = (x as i16, y as i16);
                height = 'z';
            }
            grid.insert((x as i16, y as i16), height);
        }
    }
    println!("{}", get_dist(&grid, start, end).unwrap());
}

fn part_2() {
    let mut grid: HashMap<(i16, i16), char> = HashMap::new();
    let mut end: (i16, i16) = (255, 255);
    let mut possible_start: Vec<(i16, i16)> = Vec::new();

    for (y, l) in fs::read_to_string("input.txt")
        .unwrap()
        .split("\n")
        .enumerate()
    {
        for (x, c) in l.chars().enumerate() {
            let mut height = c;
            if c.eq(&'S') {
                height = 'a';
            } else if c.eq(&'E') {
                end = (x as i16, y as i16);
                height = 'z';
            }
            if height == 'a' {
                possible_start.push((x as i16, y as i16));
            }
            grid.insert((x as i16, y as i16), height);
        }
    }

    println!(
        "{:?}",
        possible_start
            .iter()
            .map(|start| get_dist(&grid, *start, end))
            .filter(|dst| dst.is_some())
            .min()
            .unwrap()
            .unwrap()
    );
}

fn main() {
    bench(part_1);
    bench(part_2);
}
