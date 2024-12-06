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
fn part_1() -> HashSet<(i32, i32)> {
    let input = include_str!("input.txt");
    let mut obstacles = HashSet::new();
    let dirs: HashMap<char, (i32, i32)> =
        HashMap::from([('^', (0, -1)), ('>', (1, 0)), ('v', (0, 1)), ('<', (-1, 0))]);
    let rot = "^>v<";

    let mut guard = ('.', (0, 0)); // Initialize with a dummy value
    for (y, line) in input.lines().enumerate() {
        for (x, c) in line.chars().enumerate() {
            if c == '#' {
                obstacles.insert((x as i32, y as i32));
            } else if rot.contains(c) {
                guard = (c, (x as i32, y as i32));
            }
        }
    }
    let mut seen = HashSet::new();
    while !seen.contains(&guard) {
        seen.insert(guard);

        let mut np = (guard.1 .0 + dirs[&guard.0].0, guard.1 .1 + dirs[&guard.0].1);
        let mut d = guard.0;
        if obstacles.contains(&np) {
            let i = rot.find(d).unwrap();

            d = rot.chars().nth((i + 1) % rot.len()).unwrap();
            np = (guard.1 .0 + dirs[&d].0, guard.1 .1 + dirs[&d].1);
        }

        if !(0 <= np.0
            && np.0 < input.lines().next().unwrap().len() as i32
            && 0 <= np.1
            && np.1 < input.lines().count() as i32)
        {
            break;
        }
        guard = (d, np);
    }
    let path: HashSet<(i32, i32)> = seen.iter().map(|&(_, pos)| pos).collect();
    println!("{}", path.len());

    path
}

fn in_bounds(pos: &(i32, i32), max_x: i32, max_y: i32) -> bool {
    0 <= pos.0 && pos.0 < max_x && 0 <= pos.1 && pos.1 < max_y
}
fn is_guard_in_loop(
    guard: (char, (i32, i32)),
    obstacles: &HashSet<(i32, i32)>,
    max_x: i32,
    max_y: i32,
) -> bool {
    let dirs: HashMap<char, (i32, i32)> =
        HashMap::from([('^', (0, -1)), ('>', (1, 0)), ('v', (0, 1)), ('<', (-1, 0))]);
    let rot = "^>v<";

    let mut seen = HashSet::new();
    let mut current_guard = guard;
    while !seen.contains(&current_guard) {
        seen.insert(current_guard);
        let mut new_position = (
            current_guard.1 .0 + dirs[&current_guard.0].0,
            current_guard.1 .1 + dirs[&current_guard.0].1,
        );
        let mut current_direction = current_guard.0;

        // keep rotating until the new position is free space
        while obstacles.contains(&new_position) {
            let i = rot.find(current_direction).unwrap();
            current_direction = rot.chars().nth((i + 1) % rot.len()).unwrap();
            new_position = (
                current_guard.1 .0 + dirs[&current_direction].0,
                current_guard.1 .1 + dirs[&current_direction].1,
            );
        }

        if !in_bounds(&new_position, max_x, max_y) {
            return false;
        }

        current_guard = (current_direction, new_position);
    }

    true
}

fn part_2(path: HashSet<(i32, i32)>) {
    let input = include_str!("input.txt");
    let mut obstacles = HashSet::new();
    let (max_x, max_y) = (
        input.lines().next().unwrap().len() as i32,
        input.lines().count() as i32,
    );
    let mut guard = ('.', (0, 0)); // Initialize with a dummy value

    for (y, line) in input.lines().enumerate() {
        for (x, c) in line.chars().enumerate() {
            if c == '#' {
                obstacles.insert((x as i32, y as i32));
            } else if "^>v<".contains(c) {
                guard = (c, (x as i32, y as i32));
            }
        }
    }

    let result: usize = path
        .iter()
        .filter(|&t| {
            let mut obs_clone = obstacles.clone();
            obs_clone.insert(*t);
            is_guard_in_loop(guard, &obs_clone, max_x, max_y)
        })
        .count();

    println!("{}", result);
}

fn main() {
    let path = bench(part_1);
    bench(|| part_2(path));
}
