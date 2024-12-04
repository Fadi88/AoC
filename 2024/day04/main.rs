use std::time;

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}
fn is_valid(grid: &Vec<Vec<char>>, y: i32, x: i32) -> bool {
    x >= 0 && x < grid[0].len() as i32 && y >= 0 && y < grid.len() as i32
}

fn check_xmas(grid: &Vec<Vec<char>>, pos: (i32, i32), d: (i32, i32)) -> bool {
    let (px, py) = pos;
    let (dx, dy) = d;

    let m = is_valid(grid, py + dy * 1, px + dx * 1)
        && grid[(py + dy * 1) as usize][(px + dx * 1) as usize] == 'M';
    let a = is_valid(grid, py + dy * 2, px + dx * 2)
        && grid[(py + dy * 2) as usize][(px + dx * 2) as usize] == 'A';
    let s = is_valid(grid, py + dy * 3, px + dx * 3)
        && grid[(py + dy * 3) as usize][(px + dx * 3) as usize] == 'S';

    m && a && s
}

fn part_1() {
    let contents = include_str!("input.txt");
    let grid: Vec<Vec<char>> = contents
        .lines()
        .map(|l| l.trim().chars().collect())
        .collect();

    let mut s = 0;
    for y in 0..grid.len() {
        for x in 0..grid[0].len() {
            for dx in -1..=1 {
                for dy in -1..=1 {
                    if dx == 0 && dy == 0 {
                        continue;
                    }
                    if grid[y][x] == 'X' {
                        s += check_xmas(&grid, (x as i32, y as i32), (dx, dy)) as i32;
                    }
                }
            }
        }
    }
    println!("{}", s);
}

fn check_xmas_2(grid: &Vec<Vec<char>>, x: i32, y: i32) -> bool {
    if !((-1..=1)
        .flat_map(|dx| (-1..=1).map(move |dy| (dx, dy)))
        .filter(|(dx, dy)| *dx != 0 && *dy != 0)
        .all(|(dx, dy)| is_valid(grid, y + dy, x + dx)))
    {
        return false;
    }

    let chars = [
        grid[(y + 1) as usize][(x + 1) as usize],
        grid[(y - 1) as usize][(x - 1) as usize],
        grid[(y - 1) as usize][(x + 1) as usize],
        grid[(y + 1) as usize][(x - 1) as usize],
    ];

    chars.iter().filter(|&&c| c == 'S').count() == 2
        && chars.iter().filter(|&&c| c == 'M').count() == 2
        && chars[0] != chars[1]
}

fn part_2() {
    let contents = include_str!("input.txt");
    let grid: Vec<Vec<char>> = contents
        .lines()
        .map(|l| l.trim().chars().collect())
        .collect();

    let mut s = 0;
    for y in 0..grid.len() {
        for x in 0..grid[0].len() {
            if grid[y][x] == 'A' {
                s += check_xmas_2(&grid, x as i32, y as i32) as i32;
            }
        }
    }
    println!("{}", s);
}

fn main() {
    bench(part_1);
    bench(part_2);
}
