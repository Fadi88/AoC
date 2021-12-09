use std::collections::{HashSet, VecDeque};
use std::fs;
use std::time;

static DELTAS: [(i32, i32); 4] = [(0, 1), (0, -1), (1, 0), (-1, 0)];

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}

fn part_1() {
    let mut heightmap: Vec<Vec<u32>> = Vec::new();
    for l in fs::read_to_string("day09/input.txt").unwrap().lines() {
        heightmap.push(
            l.chars()
                .collect::<Vec<char>>()
                .iter()
                .map(|x| x.to_digit(10).unwrap())
                .collect::<Vec<u32>>(),
        );
    }

    let mut cnt = 0;
    for x in 0..(heightmap.len() as i32) {
        for y in 0..(heightmap[x as usize].len() as i32) {
            let mut is_low = true;
            for (dx, dy) in DELTAS {
                if x + dx >= 0
                    && y + dy >= 0
                    && x + dx < heightmap.len() as i32
                    && y + dy < heightmap[x as usize].len() as i32
                {
                    is_low &= heightmap[x as usize][y as usize]
                        < heightmap[(x + dx) as usize][(y + dy) as usize];
                }
            }
            if is_low {
                cnt += 1 + heightmap[x as usize][y as usize];
            }
        }
    }
    println!("part 1 : {}", cnt);
}
fn discover_point(
    x: i32,
    y: i32,
    heightmap: &Vec<Vec<u32>>,
    visited: &mut HashSet<(i32, i32)>,
) -> u32 {
    let mut ret: HashSet<(i32, i32)> = HashSet::new();
    let mut to_visit: VecDeque<(i32, i32)> = VecDeque::new();

    to_visit.push_back((x, y));

    while !to_visit.is_empty() {
        let (nx, ny) = to_visit.pop_front().unwrap();
        visited.insert((nx, ny));
        if heightmap[nx as usize][ny as usize] < 9 {
            ret.insert((nx, ny));

            for (dx, dy) in DELTAS {
                if nx + dx >= 0
                    && ny + dy >= 0
                    && nx + dx < heightmap.len() as i32
                    && ny + dy < heightmap[nx as usize].len() as i32
                {
                    if !&visited.contains(&(nx + dx, ny + dy)) {
                        to_visit.push_back((nx + dx, ny + dy));
                    }
                }
            }
        }
    }
    ret.len() as u32
}

fn part_2() {
    let mut heightmap: Vec<Vec<u32>> = Vec::new();
    let mut sink_sizes: Vec<u32> = Vec::new();
    for l in fs::read_to_string("day09/input.txt").unwrap().lines() {
        heightmap.push(
            l.chars()
                .collect::<Vec<char>>()
                .iter()
                .map(|x| x.to_digit(10).unwrap())
                .collect::<Vec<u32>>(),
        );
    }

    let mut visisted: HashSet<(i32, i32)> = HashSet::new();

    for x in 0..(heightmap.len() as i32) {
        for y in 0..(heightmap[x as usize].len() as i32) {
            for (dx, dy) in DELTAS {
                if (x + dx) >= 0
                    && (y + dy) >= 0
                    && (x + dx) < heightmap.len() as i32
                    && (y + dy) < heightmap[x as usize].len() as i32
                {
                    let nx = x + dx;
                    let ny = y + dy;

                    if !visisted.contains(&(nx, ny)) {
                        sink_sizes.push(discover_point(nx, ny, &heightmap, &mut visisted));
                        visisted.insert((nx, ny));
                    }
                }
            }
        }
    }
    sink_sizes.sort();
    println!(
        "part 2 : {}",
        sink_sizes.iter().rev().take(3).product::<u32>()
    );
}

fn main() {
    bench(part_1);
    bench(part_2);
}
