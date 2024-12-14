use regex::Regex;
use std::collections::HashSet;
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

fn simulate_robots(robots: &Vec<((i32, i32), (i32, i32))>, t: i32) -> Vec<(i32, i32)> {
    let max_x = 101;
    let max_y = 103;

    robots
        .iter()
        .map(|&((rx, ry), (vx, vy))| {
            (
                (rx + t * vx).rem_euclid(max_x),
                (ry + t * vy).rem_euclid(max_y),
            )
        })
        .collect()
}

fn count_quadrant(robots: &Vec<(i32, i32)>) -> i32 {
    let (mut c1, mut c2, mut c3, mut c4) = (0, 0, 0, 0);
    let max_x = 101;
    let max_y = 103;

    for &(rx, ry) in robots {
        if rx < max_x / 2 && ry < max_y / 2 {
            c1 += 1;
        } else if rx > max_x / 2 && ry < max_y / 2 {
            c2 += 1;
        } else if rx < max_x / 2 && ry > max_y / 2 {
            c3 += 1;
        } else if rx > max_x / 2 && ry > max_y / 2 {
            c4 += 1;
        }
    }
    c1 * c2 * c3 * c4
}

fn part_1() {
    let input_file = include_str!("input.txt");
    let re = Regex::new(r"-?\d+").unwrap();

    let mut robots = Vec::new();

    for line in input_file.lines() {
        let p: Vec<i32> = re
            .captures_iter(line)
            .map(|cap| cap[0].parse().unwrap())
            .collect();
        robots.push(((p[0], p[1]), (p[2], p[3])));
    }

    let robots = simulate_robots(&robots, 100);
    println!("{}", count_quadrant(&robots));
}

fn count_in_formation(robots: &HashSet<(i32, i32)>) -> usize {
    let deltas = [(1, 0), (0, 1), (-1, 0), (0, -1)];

    let mut touching = 0;
    for &(rx, ry) in robots {
        for (dx, dy) in deltas.iter() {
            if robots.contains(&(rx + dx, ry + dy)) {
                touching += 1;
                break;
            }
        }
    }
    touching
}

fn part_2() {
    let input_file = include_str!("input.txt");
    let re = Regex::new(r"-?\d+").unwrap();

    let mut robots = Vec::new();
    for line in input_file.lines() {
        let p: Vec<i32> = re
            .captures_iter(line)
            .map(|cap| cap[0].parse().unwrap())
            .collect();
        robots.push(((p[0], p[1]), (p[2], p[3])));
    }

    let mut t = 1;
    loop {
        let positions: HashSet<(i32, i32)> = simulate_robots(&robots, t).into_iter().collect();
        if count_in_formation(&positions) >= positions.len() / 2 {
            break;
        }
        t += 1;
    }
    println!("{}", t);
}

fn main() {
    bench(part_1);
    bench(part_2);
}
