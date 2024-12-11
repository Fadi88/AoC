use std::time::Instant;
use std::collections::HashSet;

fn bench<F, R>(f: F) -> R
where
    F: FnOnce() -> R,
{
    let t0 = Instant::now();
    let result = f(); // Call the function and store the result
    println!("time used: {:?}", Instant::now().duration_since(t0));
    result // Return the result of the function
}

fn is_valid(grid: &Vec<Vec<u32>>, x: i32, y: i32) -> bool {
    x >= 0 && x < grid[0].len() as i32 && y >= 0 && y < grid.len() as i32
}

fn explore(grid: &Vec<Vec<u32>>, p: (i32, i32)) -> (u32, usize) {
    let deltas = [(0, 1), (0, -1), (1, 0), (-1, 0)];

    let mut to_visit = vec![p];
    let mut valid_path = 0;
    let mut nines = HashSet::new();

    while let Some((px, py)) = to_visit.pop() {
        let height = grid[py as usize][px as usize];

        if height == 9 {
            valid_path += 1;
            nines.insert((px, py));
            continue;
        }

        for (dx, dy) in deltas {
            let nx = px + dx;
            let ny = py + dy;
            if is_valid(grid, nx, ny) && grid[ny as usize][nx as usize] == height + 1 {
                to_visit.push((nx, ny));
            }
        }
    }

    (valid_path, nines.len())
}

fn part_1() {
    let input = include_str!("input.txt"); // Use include_str! here
    let grid: Vec<Vec<u32>> = input
        .lines()
        .map(|line| line.chars().map(|c| c.to_digit(10).unwrap()).collect())
        .collect();

    let mut s = 0;
    for (y, row) in grid.iter().enumerate() {
        for (x, &h) in row.iter().enumerate() {
            if h == 0 {
                let (_, n) = explore(&grid, (x as i32, y as i32));
                s += n;
            }
        }
    }

    println!("{}", s);
}

fn part_2() {
    let input = include_str!("input.txt"); // Use include_str! here
    let grid: Vec<Vec<u32>> = input
        .lines()
        .map(|line| line.chars().map(|c| c.to_digit(10).unwrap()).collect())
        .collect();

    let mut s = 0;
    for (y, row) in grid.iter().enumerate() {
        for (x, &h) in row.iter().enumerate() {
            if h == 0 {
                let (u, _) = explore(&grid, (x as i32, y as i32));
                s += u;
            }
        }
    }

    println!("{}", s);
}

fn main() {
    bench(part_1);
    bench(part_2);
}
