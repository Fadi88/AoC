use std::time;

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}

fn get_fuel_p1(input: &[i32], i: i32) -> i32 {
    input
        .iter()
        .map(|x| (x - i).abs())
        .collect::<Vec<_>>()
        .iter()
        .sum()
}

fn part_1() {
    let input = include_str!("input.txt")
        .split(',')
        .map(|x| x.parse::<i32>().unwrap())
        .collect::<Vec<_>>();

    let p1 = *(0..=*input.iter().max().unwrap())
        .collect::<Vec<_>>()
        .iter()
        .map(|v| get_fuel_p1(&input, v.clone()))
        .collect::<Vec<_>>()
        .iter()
        .min()
        .unwrap();

    println!("part 1 : {:?}", p1);
}

fn get_fuel_p2(input: &[i32], i: i32) -> i32 {
    input
        .iter()
        .map(|x| {
            let dist = (x - i).abs();
            dist * (dist + 1) / 2
        })
        .collect::<Vec<_>>()
        .iter()
        .sum()
}

fn part_2() {
    let input = include_str!("input.txt")
        .split(',')
        .map(|x| x.parse::<i32>().unwrap())
        .collect::<Vec<_>>();

    let p2 = *(0..=*input.iter().max().unwrap())
        .collect::<Vec<_>>()
        .iter()
        .map(|v| get_fuel_p2(&input, v.clone()))
        .collect::<Vec<_>>()
        .iter()
        .min()
        .unwrap();

    println!("part 2 : {:?}", p2);
}

fn main() {
    bench(part_1);
    bench(part_2);
}
