use std::collections::{HashMap, HashSet};
use std::time;

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
enum Direction {
    Up,
    Right,
    Down,
    Left,
}

impl Direction {
    fn to_tuple(self) -> (i32, i32) {
        match self {
            Direction::Up => (0, -1),
            Direction::Right => (1, 0),
            Direction::Down => (0, 1),
            Direction::Left => (-1, 0),
        }
    }

    fn rotate(self) -> Direction {
        match self {
            Direction::Up => Direction::Right,
            Direction::Right => Direction::Down,
            Direction::Down => Direction::Left,
            Direction::Left => Direction::Up,
        }
    }
}

#[derive(Debug, Hash, PartialEq, Eq, Clone, Copy)]
struct Guard {
    direction: Direction,
    position: (i32, i32),
}

fn part_1() -> HashSet<(i32, i32)> {
    let mut obstacles: HashSet<(i32, i32)> = HashSet::new();
    let mut guard = None;

    let dirs = HashMap::from([
        ('^', Direction::Up),
        ('>', Direction::Right),
        ('v', Direction::Down),
        ('<', Direction::Left),
    ]);

    // Read the input file
    let file = include_str!("input.txt");
    let lines: Vec<&str> = file.lines().collect();
    for (y, line) in lines.iter().enumerate() {
        for (x, c) in line.chars().enumerate() {
            if c == '#' {
                obstacles.insert((x as i32, y as i32));
            } else if let Some(dir) = dirs.get(&c) {
                guard = Some(Guard {
                    direction: *dir,
                    position: (x as i32, y as i32),
                });
            }
        }
    }

    let mut seen: HashSet<Guard> = HashSet::new();
    let mut guard = guard.unwrap();

    while !seen.contains(&guard) {
        seen.insert(guard);

        // Move the guard
        let (dx, dy) = guard.direction.to_tuple();
        let mut np = (guard.position.0 + dx, guard.position.1 + dy);
        let mut direction = guard.direction;

        if obstacles.contains(&np) {
            direction = direction.rotate();
            let (dx, dy) = direction.to_tuple();
            np = (guard.position.0 + dx, guard.position.1 + dy);
        }

        // Check if the new position is out of bounds
        if np.0 < 0 || np.1 < 0 || np.0 >= lines.len() as i32 || np.1 >= lines[0].len() as i32 {
            break;
        }

        guard = Guard {
            direction,
            position: np,
        };
    }

    // Collect the path
    let path: HashSet<(i32, i32)> = seen.iter().map(|g| g.position).collect();
    println!("{}", path.len());

    path
}

fn is_guard_in_loop(
    guard: (char, (i32, i32)),
    obstacles: &HashSet<(i32, i32)>,
    max_x: i32,
    max_y: i32,
) -> bool {
    let mut seen: HashSet<Guard> = HashSet::new();
    let mut guard = guard;

    while !seen.contains(&guard) {
        seen.insert(guard);

        // Calculate the new position based on the current direction
        let (dx, dy) = guard.direction.to_tuple();
        let mut new_position = (guard.position.0 + dx, guard.position.1 + dy);
        let mut current_direction = guard.direction;

        // Check for obstacle and rotate if necessary
        if obstacles.contains(&new_position) {
            for _ in 0..4 {
                current_direction = current_direction.rotate();
                let (dx, dy) = current_direction.to_tuple();
                new_position = (guard.position.0 + dx, guard.position.1 + dy);
                if !obstacles.contains(&new_position) {
                    break;
                }
            }
        }

        // Check if the new position is out of bounds
        if !(0 <= new_position.0 && new_position.0 < max_x && 0 <= new_position.1 && new_position.1 < max_y) {
            return false; // Out of bounds, no loop
        }

        guard = Guard {
            direction: current_direction,
            position: new_position,
        };
    }

    true // The guard is in a loop
}
fn part_2(path: &HashSet<(i32, i32)>) {
    let mut max_x = 0;
    let mut max_y = 0;
    let mut guard = (' ', (0, 0));
    let mut obstacles = HashSet::new();

    // Read the input from file and populate the obstacles and guard position
    let input = include_str!("input.txt");
    for (y, line) in input.lines().enumerate() {
        max_y = y as i32 + 1; // max_y is the number of rows (1-based)
        max_x = line.trim().len() as i32; // max_x is the length of the first row (column count)
        for (x, c) in line.trim().chars().enumerate() {
            if c == '#' {
                obstacles.insert((x as i32, y as i32));
            } else if c == '^' {
                guard = (c, (x as i32, y as i32));
            }
        }
    }

    // Check if the guard goes into a loop after visiting each point in the path
    let result: i32 = path.iter()
        .map(|&t| if is_guard_in_loop(guard, &obstacles, max_x, max_y) { 1 } else { 0 })
        .sum();

    println!("{}", result);
}

fn main() {
    let path = part_1();
    part_2(&path);
}
