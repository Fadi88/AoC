use std::collections::HashSet;
use std::time;

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}

fn part_1() {
    let mut buf: Vec<Vec<u16>> = Vec::new();
    for l in include_str!("input.txt").split("\n") {
        buf.push(
            l.chars()
                .map(|x| x.to_digit(10).unwrap() as u16)
                .collect::<Vec<_>>(),
        );
    }

    let grid = buf;
    let mut vis: HashSet<(usize, usize)> = HashSet::new();

    for y in 0..grid.len() {
        for x in 0..grid[0].len() {
            if x == 0 || x == grid[0].len() - 1 || y == 0 || y == grid.len() - 1 {
                vis.insert((x, y));
            } else {
                let left = grid[y][0..x].iter().copied().rev().collect::<Vec<_>>();
                let right = grid[y][x + 1..grid[0].len()].to_vec();

                let top = grid[0..y].iter().map(|r| r[x]).collect::<Vec<_>>();
                let bottom = grid[y + 1..grid.len()]
                    .iter()
                    .map(|r| r[x])
                    .collect::<Vec<_>>();

                if left.iter().all(|v| *v < grid[y][x])
                    || right.iter().all(|v| *v < grid[y][x])
                    || top.iter().all(|v| *v < grid[y][x])
                    || bottom.iter().all(|v| *v < grid[y][x])
                {
                    vis.insert((x, y));
                }
            }
        }
    }

    println!("{}", vis.len());
}

fn get_score(val: u32, direction: &Vec<u32>) -> u32 {
    let mut score = 0;
    for tree in direction {
        if val > *tree {
            score += 1;
        } else {
            return score + 1;
        }
    }
    return score;
}

fn part_2() {
    let mut buf: Vec<Vec<u32>> = Vec::new();
    for l in include_str!("input.txt").split("\n") {
        buf.push(
            l.chars()
                .map(|x| x.to_digit(10).unwrap() as u32)
                .collect::<Vec<_>>(),
        );
    }

    let grid = buf;
    let mut score: Vec<Vec<u32>> = Vec::new();

    for y in 0..grid.len() {
        let mut tmp: Vec<u32> = Vec::new();
        for x in 0..grid[0].len() {
            let left = grid[y][0..x].iter().copied().rev().collect::<Vec<_>>();
            let right = grid[y][x + 1..grid[0].len()].to_vec();

            let top = grid[0..y].iter().map(|r| r[x]).rev().collect::<Vec<_>>();
            let bottom = grid[y + 1..grid.len()]
                .iter()
                .map(|r| r[x])
                .collect::<Vec<_>>();

            tmp.push(
                get_score(grid[y][x], &right)
                    * get_score(grid[y][x], &left)
                    * get_score(grid[y][x], &top)
                    * get_score(grid[y][x], &bottom),
            );
        }

        score.push(tmp);
    }

    println!(
        "{}",
        score.iter().map(|r| r.iter().max().unwrap()).max().unwrap()
    );
}

fn main() {
    bench(part_1);
    bench(part_2);
}
