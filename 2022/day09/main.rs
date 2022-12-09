use std::collections::{HashMap, HashSet};
use std::time;

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}

fn follow(head: &(i16, i16), tail: &(i16, i16)) -> (i16, i16) {
    let dx = head.0 - tail.0;
    let dy = head.1 - tail.1;

    if (dx.abs() > 1 && dy == 0) || (dy.abs() > 1 && dx == 0) {
        (tail.0 + (dx / 2), tail.1 + (dy / 2))
    } else if dx.abs() > 1 || dy.abs() > 1 {
        let mut around_head: HashSet<(i16, i16)> = HashSet::new();
        let mut around_tail: HashSet<(i16, i16)> = HashSet::new();

        for nx in [-1, 0, 1] {
            for ny in [-1, 0, 1] {
                if nx == 0 && ny == 0 {
                    continue;
                }
                around_head.insert((head.0 + nx, head.1 + ny));
                if nx != 0 && ny != 0 {
                    around_tail.insert((tail.0 + nx, tail.1 + ny));
                }
            }
        }
        *around_head.intersection(&around_tail).next().unwrap()
    } else {
        tail.clone()
    }
}
fn part_1() {
    let mut head: (i16, i16) = (0, 0);
    let mut tail: (i16, i16) = (0, 0);

    let mut vis: HashSet<(i16, i16)> = HashSet::new();
    let deltas: HashMap<&str, (i16, i16)> =
        HashMap::from([("R", (1, 0)), ("L", (-1, 0)), ("U", (0, 1)), ("D", (0, -1))]);

    for l in include_str!("input.txt").split("\n") {
        let mut p = l.split(" ");
        let delta = deltas.get(p.next().unwrap()).unwrap();

        for _ in 0..p.next().unwrap().parse::<usize>().unwrap() {
            head = (head.0 + delta.0, head.1 + delta.1);
            tail = follow(&head, &tail);

            vis.insert(tail.clone());
        }
    }
    println!("{}", vis.len());
}

fn part_2() {
    let mut rope: [(i16, i16); 10] = [(0, 0); 10];

    let mut vis: HashSet<(i16, i16)> = HashSet::new();
    let deltas: HashMap<&str, (i16, i16)> =
        HashMap::from([("R", (1, 0)), ("L", (-1, 0)), ("U", (0, 1)), ("D", (0, -1))]);

    for l in include_str!("input.txt").split("\n") {
        let mut p = l.split(" ");
        let delta = deltas.get(p.next().unwrap()).unwrap();

        for _ in 0..p.next().unwrap().parse::<usize>().unwrap() {
            rope[0] = (rope[0].0 + delta.0, rope[0].1 + delta.1);

            for i in 1..rope.len() {
                rope[i] = follow(&rope[i - 1], &rope[i]);
            }

            vis.insert(rope.last().unwrap().clone());
        }
    }
    println!("{}", vis.len());
}

fn main() {
    bench(part_1);
    bench(part_2);
}
