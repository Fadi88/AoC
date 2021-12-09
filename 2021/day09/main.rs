use std::fs;
use std::time;

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

    let deltas: [(i32, i32); 4] = [(0, 1), (0, -1), (1, 0), (-1, 0)];
    let mut cnt = 0;
    for x in 0..(heightmap.len() as i32) {
        for y in 0..(heightmap[x as usize].len() as i32) {
            let mut is_low = true;
            for (dx, dy) in deltas {
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

fn part_2() {
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

    let deltas: [(i32, i32); 4] = [(0, 1), (0, -1), (1, 0), (-1, 0)];
    let mut cnt = 0;
}

fn main() {
    bench(part_1);
    bench(part_2);
}
