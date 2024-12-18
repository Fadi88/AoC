use std::collections::{HashSet, VecDeque};
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

fn maze(pts: &[(i32, i32)]) -> Option<i32> {
    let start = (0, 0);
    let end = (70, 70);

    let mut seen = HashSet::new();
    let mut to_visit = VecDeque::from([(start, 0)]);

    while let Some((cp, cd)) = to_visit.pop_front() {
        if seen.contains(&cp) {
            continue;
        }

        if cp == end {
            return Some(cd);
        }

        for (dx, dy) in [(1, 0), (-1, 0), (0, 1), (0, -1)] {
            let np = (cp.0 + dx, cp.1 + dy);
            if 0 <= np.0
                && np.0 <= 70
                && 0 <= np.1
                && np.1 <= 70
                && !seen.contains(&np)
                && !pts.contains(&np)
            {
                to_visit.push_back((np, cd + 1));
            }
        }

        seen.insert(cp);
    }

    None
}

fn part_1() {
    let input_file = include_str!("input.txt");
    let pts: Vec<(i32, i32)> = input_file
        .lines()
        .map(|l| {
            let mut coords = l.split(',').map(|s| s.parse().unwrap());
            (coords.next().unwrap(), coords.next().unwrap())
        })
        .collect();

    let first_1024_pts: Vec<(i32, i32)> = pts.iter().take(1024).cloned().collect();

    match maze(&first_1024_pts) {
        Some(result) => println!("{}", result),
        None => println!("No path found!"),
    }
}

fn part_2() {
    let input_file = include_str!("input.txt");
    let pts: Vec<(i32, i32)> = input_file
        .lines()
        .map(|l| {
            let mut coords = l.split(',').map(|s| s.parse().unwrap());
            (coords.next().unwrap(), coords.next().unwrap())
        })
        .collect();

    let mut lower = 1024;
    let mut upper = pts.len();

    while upper - lower > 1 {
        let l = (upper + lower) / 2;

        if maze(&pts[..l]).is_some() {
            lower = l;
        } else {
            upper = l;
        }
    }

    println!("{:?}", pts[upper - 1]);
}

fn main() {
    bench(part_1);
    bench(part_2);
}
