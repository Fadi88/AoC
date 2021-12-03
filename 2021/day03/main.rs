use std::fs;
use std::io::{prelude::*, BufReader};
use std::time;

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}

fn part_1() {
    let ls: Vec<Vec<char>> = BufReader::new(fs::File::open("day03/input.txt").unwrap())
        .lines()
        .map(|l| l.unwrap().chars().collect())
        .collect();

    let mut cnt: Vec<u16> = vec![0; ls[0].len()];

    for bit in 0..ls[0].len() {
        let mut ones: u16 = 0;

        for l in &ls {
            if l[bit] == '1' {
                ones += 1;
            }
        }
        cnt[bit] = ones;
    }

    let gamma = String::from_iter(cnt.into_iter().map(|bit| {
        if bit as usize > ls.len() / 2 {
            return '1';
        } else {
            return '0';
        }
    }));

    let epsilon = gamma.replace('0', "x").replace('1', "0").replace("x", "1");
    let gamma_v = u32::from_str_radix(&gamma, 2).unwrap();
    let epsilon_v = u32::from_str_radix(&epsilon, 2).unwrap();
    println!("part 1 : {}", gamma_v * epsilon_v)
}

fn part_2() {
    let ls: Vec<Vec<char>> = BufReader::new(fs::File::open("day03/input.txt").unwrap())
        .lines()
        .map(|l| l.unwrap().chars().collect())
        .collect();

    let mut nums_oxy = ls.clone();

    for bit in 0..ls[0].len() {
        let bits = nums_oxy.iter().map(|x| x[bit]).collect::<Vec<_>>();

        let c0 = bits.iter().filter(|x| **x == '0').count();
        let c1 = bits.iter().filter(|x| **x == '1').count();

        let keep = if c1 >= c0 { '1' } else { '0' };

        nums_oxy.retain(|x| x[bit] == keep);
        if nums_oxy.len() == 1 {
            break;
        }
    }

    let mut nums_car = ls.clone();

    for bit in 0..ls[0].len() {
        let bits = nums_car.iter().map(|x| x[bit]).collect::<Vec<_>>();

        let c0 = bits.iter().filter(|x| **x == '0').count();
        let c1 = bits.iter().filter(|x| **x == '1').count();

        let keep = if c1 >= c0 { '0' } else { '1' };

        nums_car.retain(|x| x[bit] == keep);
        if nums_car.len() == 1 {
            break;
        }
    }

    let oxy = u32::from_str_radix(&nums_oxy[0].iter().collect::<String>(), 2).unwrap();
    let car = u32::from_str_radix(&nums_car[0].iter().collect::<String>(), 2).unwrap();

    println!("part 2 : {:?}", oxy * car);
}

fn main() {
    bench(part_1);
    bench(part_2);
}
