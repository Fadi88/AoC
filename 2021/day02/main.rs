use std::fs;
use std::time;

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}

struct Postion {
    x: i32,
    y: i32,
}

fn part_1() {
    let mut pos = Postion { x: 0, y: 0 };

    for l in fs::read_to_string("day02/input.txt").unwrap().lines() {
        let p: Vec<&str> = l.split(" ").collect();
        if p[0] == "up" {
            pos.y -= p[1].parse::<i32>().unwrap();
        } else if p[0] == "down" {
            pos.y += p[1].parse::<i32>().unwrap();
        } else if p[0] == "forward" {
            pos.x += p[1].parse::<i32>().unwrap();
        }
    }

    println!("{:?}", pos.x * pos.y);
}

fn part_2() {
    let mut pos = Postion { x: 0, y: 0 };
    let mut aim: i32 = 0;

    for l in fs::read_to_string("day02/input.txt").unwrap().lines() {
        let p: Vec<&str> = l.split(" ").collect();
        let ds = p[1].parse::<i32>().unwrap();
        if p[0] == "up" {
            aim -= ds;
        } else if p[0] == "down" {
            aim += ds;
        } else if p[0] == "forward" {
            pos.x += ds;
            pos.y += ds * aim;
        }
    }

    println!("{:?}", pos.x * pos.y);
}

fn main() {
    bench(part_1);
    bench(part_2);
}
