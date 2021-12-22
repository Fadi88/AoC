use regex::Regex;
use std::cmp::{max, min};
use std::collections::HashSet;
use std::time;

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}

fn part_1() {
    let re = Regex::new(r".*=(-?\d+)\.+(-?\d+).*=(-?\d+)\.+(-?\d+).*=(-?\d+)\.+(-?\d+)").unwrap();
    let mut pts: HashSet<(i32, i32, i32)> = HashSet::new();

    for l in include_str!("input.txt").split("\n") {
        let t: Vec<_> = re
            .captures(l)
            .unwrap()
            .iter()
            .skip(1)
            .map(|x| x.unwrap().as_str().parse::<i32>().unwrap())
            .collect();

        if t[0] > 50 || t[1] < -50 || t[2] > 50 || t[3] < -50 || t[4] > 50 || t[5] < -50 {
            continue;
        }

        for x in max(t[0], -50)..min(50, t[1] + 1) {
            for y in max(t[2], -50)..min(50, t[3] + 1) {
                for z in max(t[4], -50)..min(50, t[5] + 1) {
                    if l.contains("on") {
                        pts.insert((x, y, z));
                    } else {
                        pts.remove(&(x, y, z));
                    }
                }
            }
        }
    }
    println!("{}", pts.len());
}
fn does_line_intersect(x0: i64, x1: i64, ox0: i64, ox1: i64) -> bool {
    (x0 <= ox0 && ox0 <= x1)
        || (x0 <= ox1 && ox1 <= x1)
        || (ox0 <= x0 && x0 <= ox1)
        || (ox0 <= x1 && x1 <= ox1)
}

fn get_line_intersection(p0: i64, p1: i64, op0: i64, op1: i64) -> (i64, i64) {
    let r0 = if op0 < p0 { p0 } else { op0 };
    let r1 = if op1 < p1 { op1 } else { p1 };

    (r0, r1)
}

struct Cuboid {
    x0: i64,
    x1: i64,
    y0: i64,
    y1: i64,
    z0: i64,
    z1: i64,

    off: Vec<Cuboid>,
}

impl Cuboid {
    pub fn new(x0: i64, x1: i64, y0: i64, y1: i64, z0: i64, z1: i64) -> Self {
        return Cuboid {
            x0: x0,
            x1: x1,
            y0: y0,
            y1: y1,
            z0: z0,
            z1: z1,

            off: Vec::new(),
        };
    }

    fn is_intresecting(&self, other: &Cuboid) -> bool {
        does_line_intersect(self.x0, self.x1, other.x0, other.x1)
            && does_line_intersect(self.y0, self.y1, other.y0, other.y1)
            && does_line_intersect(self.z0, self.z1, other.z0, other.z1)
    }

    pub fn substraction(&mut self, other: &Cuboid) {
        if self.is_intresecting(other) {
            let x = get_line_intersection(self.x0, self.x1, other.x0, other.x1);
            let y = get_line_intersection(self.y0, self.y1, other.y0, other.y1);
            let z = get_line_intersection(self.z0, self.z1, other.z0, other.z1);

            self.off.iter_mut().for_each(|x| x.substraction(other));
            self.off.push(Cuboid::new(x.0, x.1, y.0, y.1, z.0, z.1));
        }
    }

    pub fn volume(&self) -> u128 {
        ((self.x1 - self.x0 + 1) as u128
            * (self.y1 - self.y0 + 1) as u128
            * (self.z1 - self.z0 + 1) as u128)
            - self.off.iter().map(|x| x.volume()).sum::<u128>()
    }
}

fn part_2() {
    let re = Regex::new(r".*=(-?\d+)\.+(-?\d+).*=(-?\d+)\.+(-?\d+).*=(-?\d+)\.+(-?\d+)").unwrap();

    let mut cubiods: Vec<Cuboid> = Vec::new();
    for l in include_str!("input.txt").split("\n") {
        let t: Vec<_> = re
            .captures(l)
            .unwrap()
            .iter()
            .skip(1)
            .map(|x| x.unwrap().as_str().parse::<i64>().unwrap())
            .collect();
        let new_c = Cuboid::new(t[0], t[1], t[2], t[3], t[4], t[5]);
        cubiods.iter_mut().for_each(|x| x.substraction(&new_c));
        if l.contains("on") {
            cubiods.push(new_c);
        }
    }
    let s = cubiods.iter().map(|x| x.volume() as u128).sum::<u128>();

    println!("{}", s);
}

fn main() {
    bench(part_1);
    bench(part_2);
}
