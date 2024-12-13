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

fn is_valid(p: (i32, i32), max_x: i32, max_y: i32) -> bool {
    let (x, y) = p;
    0 <= x && x < max_x && 0 <= y && y < max_y
}

fn flood_fill(grid: &Vec<Vec<char>>, p: (i32, i32)) -> HashSet<(i32, i32)> {
    let max_x = grid[0].len() as i32;
    let max_y = grid.len() as i32;

    let (start_x, start_y) = p;
    let crop = grid[start_y as usize][start_x as usize];

    let mut visited = HashSet::new();
    let mut to_visit = vec![p];

    while let Some((x, y)) = to_visit.pop() {
        visited.insert((x, y));

        for (dx, dy) in [(1, 0), (-1, 0), (0, 1), (0, -1)] {
            let nx = x + dx;
            let ny = y + dy;
            if is_valid((nx, ny), max_x, max_y)
                && grid[ny as usize][nx as usize] == crop
                && !visited.contains(&(nx, ny))
            {
                to_visit.push((nx, ny));
            }
        }
    }

    visited
}

fn perimeter(points: &HashSet<(i32, i32)>) -> u32 {
    let deltas = [(1, 0), (-1, 0), (0, 1), (0, -1)];
    points
        .iter()
        .flat_map(|(x, y)| {
            deltas
                .iter()
                .map(move |(dx, dy)| (x + dx, y + dy))
                .filter(|new_p| !points.contains(new_p))
        })
        .count() as u32
}

fn part_1() {
    let input = include_str!("input.txt");
    let grid: Vec<Vec<char>> = input.lines().map(|line| line.chars().collect()).collect();

    let mut crops: Vec<HashSet<(i32, i32)>> = Vec::new();
    let mut visited = HashSet::new();
    for (y, row) in grid.iter().enumerate() {
        for (x, &_h) in row.iter().enumerate() {
            let p = (x as i32, y as i32);
            if !visited.contains(&p) && !crops.iter().any(|v| v.contains(&p)) {
                let v = flood_fill(&grid, p);
                crops.push(v.clone()); // Clone v to avoid move
                visited.extend(v);
            }
        }
    }

    let result: u32 = crops.iter().map(|v| (v.len() as u32) * perimeter(v)).sum();
    println!("{}", result);
}

fn get_boundaries(points: &HashSet<(i32, i32)>) -> HashSet<(i32, i32)> {
    let deltas = [(1, 0), (-1, 0), (0, 1), (0, -1)];
    points
        .iter()
        .flat_map(|(x, y)| {
            deltas
                .iter()
                .map(move |(dx, dy)| (x + dx, y + dy))
                .filter(|new_p| !points.contains(new_p))
        })
        .collect()
}

fn count_corners(region: &HashSet<(i32, i32)>) -> usize {
    let mut corners = HashSet::new();
    let kernels = [
        [(-1, 0), (0, -1), (-1, -1)], // upper left
        [(1, 0), (0, -1), (1, -1)],   // upper right
        [(-1, 0), (0, 1), (-1, 1)],   // lower left
        [(1, 0), (0, 1), (1, 1)],     // lower right
    ];

    // get outer corners
    for &(px, py) in region {
        for (i, kernel) in kernels.iter().enumerate() {
            let vals: Vec<(i32, i32)> = kernel.iter().map(|(kx, ky)| (px + kx, py + ky)).collect();
            if vals.iter().all(|v| !region.contains(v)) {
                corners.insert((px, py, i));
            }
        }
    }

    let inner_kernels = [
        [(-1, 0), (0, -1)],
        [(-1, 0), (0, 1)],
        [(1, 0), (0, -1)],
        [(1, 0), (0, 1)],
    ];
    let mut inner_corners = HashSet::new();
    // get inner corners
    for &(px, py) in &get_boundaries(region) {
        for (i, kernel) in inner_kernels.iter().enumerate() {
            let vals: Vec<(i32, i32)> = kernel.iter().map(|(kx, ky)| (px + kx, py + ky)).collect();
            if vals.iter().all(|v| region.contains(v)) {
                let (dx, dy) = (kernel[0].0 + kernel[1].0, kernel[0].1 + kernel[1].1);
                if region.contains(&(px + dx, py + dy)) {
                    inner_corners.insert((px + dx, py + dy, i));
                } else {
                    let ((v1x, v1y), (v2x, v2y)) = (vals[0], vals[1]);
                    let (dx, dy) = (v1x - v2x, v1y - v2y);
                    let d1 = [(-dx, 0), (0, dy)];
                    let d2 = [(dx, 0), (0, -dy)];

                    inner_corners.insert((
                        v1x,
                        v1y,
                        inner_kernels.iter().position(|&x| x == d1).unwrap(),
                    ));
                    inner_corners.insert((
                        v2x,
                        v2y,
                        inner_kernels.iter().position(|&x| x == d2).unwrap(),
                    ));
                }
            }
        }
    }

    corners.len() + inner_corners.len()
}

fn part_2() {
    let input = include_str!("input.txt");
    let grid: Vec<Vec<char>> = input.lines().map(|line| line.chars().collect()).collect();

    let mut crops: Vec<HashSet<(i32, i32)>> = Vec::new();
    let mut visited = HashSet::new();
    for (y, row) in grid.iter().enumerate() {
        for (x, _) in row.iter().enumerate() {
            let p = (x as i32, y as i32);
            if !visited.contains(&p) {
                let v = flood_fill(&grid, p);
                crops.push(v.clone());
                visited.extend(v);
            }
        }
    }

    let result: usize = crops.iter().map(|v| v.len() * count_corners(v)).sum();
    println!("{}", result);
}

fn main() {
    bench(part_1);
    bench(part_2);
}
