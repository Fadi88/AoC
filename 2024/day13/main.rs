use regex::Regex;
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

fn solve_linear_system(a: (u32, u32), b: (u32, u32), p: (u32, u32), delta: u64) -> (f64, f64) {
    let (ax, ay) = (a.0 as f64, a.1 as f64);
    let (bx, by) = (b.0 as f64, b.1 as f64);
    let (mut px, mut py) = (p.0 as f64, p.1 as f64);
    let delta = delta as f64;

    px += delta;
    py += delta;

    let det = ax * by as f64 - ay * bx as f64;

    let n1 = (px * by - py * bx) / det;
    let n2 = (py * ax - px * ay) / det;
    (n1, n2)
}
fn part_1() {
    let input = include_str!("input.txt");
    let mut machines = Vec::new();
    let re = Regex::new(r"\d+").unwrap();

    for group in input.split("\n\n") {
        let numbers: Vec<u32> = re
            .find_iter(group)
            .filter_map(|mat| mat.as_str().parse().ok())
            .collect();

        if numbers.len() == 6 {
            machines.push((
                (numbers[0], numbers[1]),
                (numbers[2], numbers[3]),
                (numbers[4], numbers[5]),
            ));
        }
    }

    let mut tokens = 0;

    for m in &machines {
        let a = m.0;
        let b = m.1;
        let p = m.2;

        let (n1, n2) = solve_linear_system(a, b, p, 0);

        if n1.fract() == 0.0
            && n2.fract() == 0.0
            && (0..100).contains(&(n1 as i32))
            && (0..100).contains(&(n2 as i32))
        {
            tokens += 3 * n1 as i32 + n2 as i32;
        }
    }

    println!("{}", tokens);
}

fn part_2() {
    let input = include_str!("input.txt");
    let mut machines = Vec::new();
    let re = Regex::new(r"\d+").unwrap();

    for group in input.split("\n\n") {
        let numbers: Vec<u32> = re
            .find_iter(group)
            .filter_map(|mat| mat.as_str().parse().ok())
            .collect();

        if numbers.len() == 6 {
            machines.push((
                (numbers[0], numbers[1]),
                (numbers[2], numbers[3]),
                (numbers[4], numbers[5]),
            ));
        }
    }

    let mut tokens = 0;

    for m in &machines {
        let a = m.0;
        let b = m.1;
        let p = m.2;

        let (n1, n2) = solve_linear_system(a, b, p, 10000000000000);
        if n1.fract() == 0.0 && n2.fract() == 0.0 {
            tokens += 3 * n1 as u64 + n2 as u64;
        }
    }
    println!("{}", tokens);
}

fn main() {
    bench(part_1);
    bench(part_2);
}
