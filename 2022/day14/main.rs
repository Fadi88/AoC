use std::collections::HashMap;
use std::fs;
use std::time;

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}

fn move_down(pos: &(i32, i32)) -> (i32, i32) {
    (pos.0, pos.1 + 1)
}

fn move_left(pos: &(i32, i32)) -> (i32, i32) {
    (pos.0 - 1, pos.1 + 1)
}

fn move_right(pos: &(i32, i32)) -> (i32, i32) {
    (pos.0 + 1, pos.1 + 1)
}

fn part_1() {
    let mut particles: HashMap<(i32, i32), char> = HashMap::new();

    for l in fs::read_to_string("input.txt").unwrap().lines() {
        let segments = l
            .split(" -> ")
            .map(|x| {
                x.split(",")
                    .map(|p| p.parse::<i32>().unwrap())
                    .collect::<Vec<_>>()
            })
            .collect::<Vec<_>>();

        for i in 1..segments.len() {
            let (p1, p2) = (&segments[i - 1], &segments[i]);

            if p1[0] == p2[0] {
                let min = p1[1].min(p2[1]);
                let max = p1[1].max(p2[1]);
                for y in min..=max {
                    particles.insert((p1[0], y as i32), '#');
                }
            } else if p1[1] == p2[1] {
                let min = p1[0].min(p2[0]);
                let max = p1[0].max(p2[0]);
                for x in min..=max {
                    particles.insert((x as i32, p1[1]), '#');
                }
            }
        }
    }

    let source: (i32, i32) = (500, 0);

    let max_y = particles.iter().map(|x| x.0 .1).max().unwrap();

    let mut fallen_sand: u16 = 0;

    'outer: loop {
        let mut pos = source.clone();
        loop {
            if !particles.contains_key(&move_down(&pos)) {
                pos = move_down(&pos);
            } else if !particles.contains_key(&move_left(&pos)) {
                pos = move_left(&pos);
            } else if !particles.contains_key(&move_right(&pos)) {
                pos = move_right(&pos);
            } else {
                particles.insert(pos, '0');
                fallen_sand += 1;
                break;
            }
            if pos.1 > max_y {
                break 'outer;
            }
        }
    }

    println!("{}", fallen_sand);
}

fn part_2() {
    let mut particles: HashMap<(i32, i32), char> = HashMap::new();

    for l in fs::read_to_string("input.txt").unwrap().lines() {
        let segments = l
            .split(" -> ")
            .map(|x| {
                x.split(",")
                    .map(|p| p.parse::<i32>().unwrap())
                    .collect::<Vec<_>>()
            })
            .collect::<Vec<_>>();

        for i in 1..segments.len() {
            let (p1, p2) = (&segments[i - 1], &segments[i]);

            if p1[0] == p2[0] {
                let min = p1[1].min(p2[1]);
                let max = p1[1].max(p2[1]);
                for y in min..=max {
                    particles.insert((p1[0], y as i32), '#');
                }
            } else if p1[1] == p2[1] {
                let min = p1[0].min(p2[0]);
                let max = p1[0].max(p2[0]);
                for x in min..=max {
                    particles.insert((x as i32, p1[1]), '#');
                }
            }
        }
    }

    let source: (i32, i32) = (500, 0);

    let max_y = particles.iter().map(|x| x.0 .1).max().unwrap();

    let mut fallen_sand: u16 = 0;

    'outer: loop {
        let mut pos = source.clone();
        fallen_sand += 1;
        loop {
            if !particles.contains_key(&move_down(&pos)) {
                pos = move_down(&pos);
            } else if !particles.contains_key(&move_left(&pos)) {
                pos = move_left(&pos);
            } else if !particles.contains_key(&move_right(&pos)) {
                pos = move_right(&pos);
            } else {
                particles.insert(pos, '0');
                if pos == source {
                    break 'outer;
                }
                break;
            }
            if pos.1 == 1 + max_y {
                particles.insert(pos, '0');
                break;
            }
        }
    }

    println!("{}", fallen_sand);
}

fn main() {
    bench(part_1);
    bench(part_2);
}
