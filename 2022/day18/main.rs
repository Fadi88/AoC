use std::collections::{HashSet, VecDeque};
use std::fs;
use std::time;

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}

type P3d = (i16, i16, i16);

fn part_1() {
    let mut air: HashSet<P3d> = HashSet::new();

    for l in fs::read_to_string("input.txt").unwrap().split("\n") {
        let mut p = l.split(",").map(|x| x.parse::<i16>().unwrap());
        air.insert((p.next().unwrap(), p.next().unwrap(), p.next().unwrap()));
    }

    let mut exposed = 0;

    for p in &air {
        for d in 0..3 {
            for delta in [-1, 1] {
                let mut s: [i16; 3] = [0, 0, 0];

                s[d] = delta;

                if !air.contains(&(p.0 + s[0], p.1 + s[1], p.2 + s[2])) {
                    exposed += 1;
                }
            }
        }
    }
    println!("{}", exposed);
}

fn fill(air: &HashSet<P3d>) -> HashSet<P3d> {
    let mut visited: HashSet<P3d> = HashSet::new();

    let start: P3d = (0, 0, 0);

    visited.insert(start);
    let mut to_visit: VecDeque<Vec<P3d>> = VecDeque::new();
    to_visit.push_front(Vec::from([start]));

    let mut xs: HashSet<i16> = HashSet::new();
    let mut ys: HashSet<i16> = HashSet::new();
    let mut zs: HashSet<i16> = HashSet::new();
    for p in air {
        xs.insert(p.0);
        ys.insert(p.1);
        zs.insert(p.2);
    }

    while !to_visit.is_empty() {
        let current_path = to_visit.pop_back().unwrap();
        let p = current_path.last().unwrap();

        for d in 0..3 {
            for delta in [-1, 1] {
                let mut s: [i16; 3] = [0, 0, 0];

                s[d] = delta;

                let n_p = (p.0 + s[0], p.1 + s[1], p.2 + s[2]);

                if air.contains(&n_p) {
                    continue;
                }
                if n_p.0 < -1 || n_p.0 > xs.iter().max().unwrap() + 1 {
                    continue;
                }
                if n_p.1 < -1 || n_p.1 > ys.iter().max().unwrap() + 1 {
                    continue;
                }
                if n_p.2 < -1 || n_p.2 > zs.iter().max().unwrap() + 1 {
                    continue;
                }
                if !current_path.contains(&n_p) && !visited.contains(&n_p) {
                    let mut new_path: Vec<P3d> = Vec::from(current_path.clone());
                    new_path.append(&mut Vec::from([n_p]));
                    visited.insert(n_p);
                    to_visit.push_back(new_path);
                }
            }
        }
    }
    visited
}

fn part_2() {
    let mut air: HashSet<P3d> = HashSet::new();

    for l in fs::read_to_string("input.txt").unwrap().split("\n") {
        let mut p = l.split(",").map(|x| x.parse::<i16>().unwrap());
        air.insert((p.next().unwrap(), p.next().unwrap(), p.next().unwrap()));
    }

    let mut exposed = 0;
    let exposed_surfaces = fill(&air);

    for p in &air {
        for d in 0..3 {
            for delta in [-1, 1] {
                let mut s: [i16; 3] = [0, 0, 0];

                s[d] = delta;

                let to_test = (p.0 + s[0], p.1 + s[1], p.2 + s[2]);
                if air.contains(&to_test) {
                    continue;
                }
                if exposed_surfaces.contains(&to_test) {
                    exposed += 1;
                }
            }
        }
    }
    println!("{}", exposed);
}

fn main() {
    bench(part_1);
    bench(part_2);
}
