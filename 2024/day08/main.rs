use itertools::Itertools;
use std::collections::{HashMap, HashSet};
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

fn is_valid(p: (i32, i32), max_x: i32, max_y: i32) -> bool {
    0 <= p.0 && p.0 < max_x && 0 <= p.1 && p.1 < max_y
}

fn generate_antinodes(p1: (i32, i32), p2: (i32, i32)) -> ((i32, i32), (i32, i32)) {

    let dx = p2.0 - p1.0;
    let dy = p2.1 - p1.1;

    let np1 = (p1.0 - dx, p1.1 - dy);
    let np2 = (p2.0 + dx, p2.1 + dy);
    
    (np1, np2)
}

fn part_1() {
    let input = include_str!("input.txt");
    let mut antennas: HashMap<char, HashSet<(i32, i32)>> = HashMap::new();
    let mut max_x = 0;
    let mut max_y = 0;

    for (y, line) in input.lines().enumerate() {
        max_x = line.len() as i32;
        max_y = y as i32 + 1;
        for (x, char) in line.chars().enumerate() {
            if char != '.' {
                antennas
                    .entry(char)
                    .or_insert_with(HashSet::new)
                    .insert((x as i32, y as i32));
            }
        }
    }

    let mut antinodes = HashSet::new();

    for (_a, positions) in antennas.iter() {
        for p in positions.iter().combinations(2) {
            let p1 = *p[0];
            let p2 = *p[1];

            let (np1, np2) = generate_antinodes(p1, p2);

            if is_valid(np1, max_x, max_y) {
                antinodes.insert(np1);
            }
            if is_valid(np2, max_x, max_y) {
                antinodes.insert(np2);
            }
        }
    }

    println!("{}", antinodes.len());
}

fn generate_all_antinodes(
    p1: (i32, i32),
    p2: (i32, i32),
    max_x: i32,
    max_y: i32,
) -> HashSet<(i32, i32)> {
    let mut antinodes = HashSet::new();
    let (x1, y1) = p1;
    let (x2, y2) = p2;

    for y3 in 0..max_y {
        for x3 in 0..max_x {
            if (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)).abs() == 0 {
                antinodes.insert((x3, y3));
            }
        }
    }

    antinodes
}
fn part_2() {
    let input = include_str!("input.txt");
    let mut antennas: HashMap<char, HashSet<(i32, i32)>> = HashMap::new();
    let mut max_x = 0;
    let mut max_y = 0;

    for (y, line) in input.lines().enumerate() {
        max_x = line.len() as i32;
        max_y = y as i32 + 1;
        for (x, char) in line.chars().enumerate() {
            if char != '.' {
                antennas
                    .entry(char)
                    .or_insert_with(HashSet::new)
                    .insert((x as i32, y as i32));
            }
        }
    }

    let mut antinodes = HashSet::new();

    for (_, positions) in antennas.iter() {
        for p in positions.iter().combinations(2) {
            let p1 = *p[0];
            let p2 = *p[1];

            for antinode in generate_all_antinodes(p1, p2, max_x, max_y) {
                antinodes.insert(antinode);
            }
        }
    }

    println!("{}", antinodes.len());
}

fn main() {
    bench(part_1);
    bench(part_2);
}
