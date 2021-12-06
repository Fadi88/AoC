use std::collections::HashMap;
use std::fs;
use std::time;

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}

fn part_1() {
    let mut input: Vec<_> = fs::read_to_string("day06/input.txt")
        .unwrap()
        .split(',')
        .map(|x| x.parse::<u8>().unwrap())
        .collect();

    for _ in 0..80 {
        let mut tmp: Vec<u8> = Vec::new();
        for i in 0..input.len() {
            if input[i] == 0 {
                tmp.push(6);
                tmp.push(8);
            } else {
                tmp.push(input[i] - 1);
            }
        }
        input = tmp;
    }
    println!("{:?}", input.len())
}

fn part_2() {
    let input: Vec<u8> = fs::read_to_string("day06/input.txt")
        .unwrap()
        .split(',')
        .map(|x| x.parse::<u8>().unwrap())
        .collect();

    let mut tracker: HashMap<u8, u64> = HashMap::new();

    for i in input {
        *tracker.entry(i).or_insert(0) += 1;
    }

    for _ in 0..256 {
        let mut tmp: HashMap<u8, u64> = HashMap::new();
        for i in tracker.clone().keys() {
            let x = *tracker.get(i).unwrap();
            if *i == 0 {
                *tmp.entry(6).or_insert(0) += x;
                *tmp.entry(8).or_insert(0) = x;
            } else {
                *tmp.entry(i - 1).or_insert(0) += x;
            }
        }
        tracker = tmp.clone();
    }

    println!(
        "{:?}",
        tracker
            .into_values()
            .collect::<Vec<_>>()
            .iter()
            .sum::<u64>()
    );
}
fn part2_array() {
    let input: Vec<u8> = fs::read_to_string("day06/input.txt")
        .unwrap()
        .split(',')
        .map(|x| x.parse::<u8>().unwrap())
        .collect();

    let mut tracker: [u64; 9] = [0; 9];

    for i in input {
        tracker[i as usize] += 1;
    }

    for _ in 0..256 {
        tracker.rotate_left(1);
        tracker[6] += tracker[8];
    }

    println!("{:?}" , tracker.into_iter().sum::<u64>());
}

fn main() {
    bench(part_1);
    bench(part_2);
    bench(part2_array);
}
