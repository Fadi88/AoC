use std::collections::{HashSet, VecDeque};
use std::time;

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}

fn cycle(grid: &mut [[i8; 10]; 10]) -> u16 {
    let mut total = 0;

    let deltas: [(i32, i32); 8] = [
        (0, 1),
        (0, -1),
        (1, 0),
        (1, 1),
        (1, -1),
        (-1, 0),
        (-1, 1),
        (-1, -1),
    ];

    let mut ready: VecDeque<(i32, i32)> = VecDeque::new();
    let mut visited: HashSet<(i32, i32)> = HashSet::new();

    for x in 0..grid.len() {
        for y in 0..grid[0].len() {
            grid[x][y] += 1;
            if grid[x][y] > 9 {
                ready.push_back((x as i32, y as i32));
                visited.insert((x as i32, y as i32));
            }
        }
    }

    while !ready.is_empty() {
        let (nx, ny) = ready.pop_front().unwrap();

        for (dx, dy) in deltas {
            if nx + dx >= 0
                && ny + dy >= 0
                && nx + dx < grid.len() as i32
                && ny + dy < grid[nx as usize].len() as i32
            {
                grid[(nx + dx) as usize][(ny + dy) as usize] += 1;

                if grid[(nx + dx) as usize][(ny + dy) as usize] > 9
                    && !visited.contains(&(nx + dx, ny + dy))
                {
                    ready.push_back((nx + dx, ny + dy));
                    visited.insert((nx + dx, ny + dy));
                }
            }
        }
    }

    for x in 0..grid.len() {
        for y in 0..grid[0].len() {
            if grid[x][y] > 9 {
                grid[x][y] = 0;
                total += 1;
            }
        }
    }

    return total;
}

fn part_1() {
    let mut grid: [[i8; 10]; 10] = [[0; 10]; 10];
    for (x, l) in include_str!("input.txt")
        .split("\n")
        .collect::<Vec<_>>()
        .iter()
        .enumerate()
    {
        for y in 0..l.len() {
            grid[x][y] = l.chars().nth(y).unwrap().to_digit(10).unwrap() as i8;
        }
    }
    let mut total: u16 = 0;

    for _ in 0..100 {
        total += cycle(&mut grid);
    }

    println!("part 1 : {}", total);
}

fn part_2() {
    let mut grid: [[i8; 10]; 10] = [[0; 10]; 10];
    for (x, l) in include_str!("input.txt")
        .split("\n")
        .collect::<Vec<_>>()
        .iter()
        .enumerate()
    {
        for y in 0..l.len() {
            grid[x][y] = l.chars().nth(y).unwrap().to_digit(10).unwrap() as i8;
        }
    }

    let mut cnt = 0;

    loop {
        cycle(&mut grid);
        cnt += 1;
        if grid.iter().all(|l| l.iter().all(|i| *i == 0)) {
            break;
        }
    }

    println!("part 2 : {}", cnt);
}

fn main() {
    bench(part_1);
    bench(part_2);
}
