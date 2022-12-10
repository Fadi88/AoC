use std::{collections::HashMap, time};

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}

fn part_1() {
    let mut x = 1i32;
    let mut cycle = 0i32;

    let mut strength: HashMap<i32, i32> = HashMap::new();
    for l in include_str!("input.txt").split("\n") {
        if l.contains("addx") {
            cycle += 1;
            strength.insert(cycle, x * cycle);
            cycle += 1;
            strength.insert(cycle, x * cycle);
            x += l.split(" ").last().unwrap().parse::<i32>().unwrap();
        } else {
            cycle += 1;
            strength.insert(cycle, x * cycle);
        }
    }

    println!(
        "{:?}",
        [20, 60, 100, 140, 180, 220]
            .map(|x| strength.get(&x).unwrap().clone())
            .iter()
            .sum::<i32>()
    );
}

fn part_2() {
    let mut x = 1i32;
    let mut cycle = 0i32;

    let mut xs: HashMap<i32, i32> = HashMap::new();
    for l in include_str!("input.txt").split("\n") {
        if l.contains("addx") {
            cycle += 1;
            xs.insert(cycle, x);
            cycle += 1;
            xs.insert(cycle, x);
            x += l.split(" ").last().unwrap().parse::<i32>().unwrap();
        } else {
            cycle += 1;
            xs.insert(cycle, x);
        }
    }

    let mut screen : [[char ; 40] ; 6] = [[' ' ; 40] ; 6];

    for cycle in xs{
        let x = cycle.1;

        if [x-1,x,x+1].contains(&((cycle.0 - 1) % 40)){
            screen[((cycle.0 - 1) / 40) as usize][((cycle.0-1)%40) as usize] = '0';
        }        
    }
    for l in screen{
        println!("{}",l.iter().collect::<String>());
    }
}

fn main() {
    bench(part_1);
    bench(part_2);
}
