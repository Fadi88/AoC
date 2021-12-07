use std::fs;
use std::time;

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}

fn get_fuel_p1(input: &Vec<i16>, i: i16) -> u32 {
    let res = input
        .iter()
        .map(|x| (x - i).abs() as u32)
        .collect::<Vec<_>>();

    res.iter().sum()
}

fn part_1() {
    let input = fs::read_to_string("day07/input.txt")
        .unwrap()
        .split(',')
        .map(|x| x.parse::<i16>().unwrap())
        .collect::<Vec<_>>();

    let p1 = input
        .iter()
        .map(|v| get_fuel_p1(&input, v.clone()))
        .collect::<Vec<_>>()
        .iter()
        .min()
        .unwrap()
        .clone();

    println!("part 1 : {:?}", p1);
}

fn get_fuel_p2(input: &Vec<u32>, i: u32) -> u32 {
    let res = input
        .iter()
        .map(|x| {
            let dist = ((x - i) as i32).abs();
            (dist * (dist + 1) / 2) as u32
        })
        .collect::<Vec<u32>>();

    res.iter().sum()
}

fn part_2() {
    let input = fs::read_to_string("day07/input.txt")
        .unwrap()
        .split(',')
        .map(|x| x.parse::<u32>().unwrap())
        .collect::<Vec<_>>();

    let p2 = input
        .iter()
        .map(|v| get_fuel_p2(&input, v.clone()))
        .collect::<Vec<_>>()
        .iter()
        .min()
        .unwrap()
        .clone();

    println!("part 2 : {:?}", p2);
}

fn main() {
    bench(part_1);
    bench(part_2);
}
