use std::collections::HashSet;
use std::time;

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}

fn part_1() {
    let mut east: HashSet<(u8, u8)> = HashSet::new();
    let mut south: HashSet<(u8, u8)> = HashSet::new();
    let mut max_x: u8 = 0;
    let mut max_y: u8 = 0;

    for (y, l) in include_str!("input.txt").split("\n").enumerate() {
        max_y = y as u8 + 1;
        max_x = l.len() as u8;
        for (x, c) in l.chars().enumerate() {
            if c == 'v' {
                south.insert((x as u8, y as u8));
            } else if c == '>'{
                east.insert((x as u8, y as u8));
            }
        }
    }

    let mut cnt: u16 = 0;
    loop {
        let mut new_east: HashSet<(u8, u8)> = HashSet::new();
        let mut new_south: HashSet<(u8, u8)> = HashSet::new();

        for e in &east {
            let n_p = ((e.0 + 1) % max_x, e.1);
            if !east.contains(&n_p) && !south.contains(&n_p) {
                new_east.insert(n_p);
            } else {
                new_east.insert(*e);
            }
        }

        for s in &south {
            let n_p = (s.0, (s.1 + 1) % max_y);
            if !south.contains(&n_p) && !new_east.contains(&n_p) {
                new_south.insert(n_p);
            } else {
                new_south.insert(*s);
            }
        }

        cnt += 1;
        if new_east.eq(&east) && south.eq(&new_south) {
            break;
        }

        south = new_south;
        east = new_east;
    }

    println!("{}", cnt);
}

fn part_2() {}

fn main() {
    bench(part_1);
    bench(part_2);
}
