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

fn solve_linear_system(
    coefficients: ((u32, u32), (u32, u32)),
    prize: (u32, u32),
    delta: u64,
) -> (f64, f64) {
    let ((a_x, a_y), (b_x, b_y)) = coefficients;
    let (point_x, point_y) = prize;

    let a_x = a_x as f64;
    let a_y = a_y as f64;
    let b_x = b_x as f64;
    let b_y = b_y as f64;
    let point_x = point_x as f64 + delta as f64;
    let point_y = point_y as f64 + delta as f64;

    let determinant = a_x * b_y - a_y * b_x;

    let n1 = (point_x * b_y - point_y * b_x) / determinant;
    let n2 = (point_y * a_x - point_x * a_y) / determinant;

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
        let (n1, n2) = solve_linear_system((m.0, m.1), m.2, 0);

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

        let (n1, n2) = solve_linear_system((m.0, m.1), m.2, 10000000000000);
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
