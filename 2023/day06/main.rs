use std::time;

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}

fn part_1() {
    let mut input: Vec<Vec<u16>> = Vec::new();

    for l in include_str!("input.txt").split("\n") {
        let t = l
            .split_whitespace()
            .into_iter()
            .skip(1)
            .map(|num| num.parse::<u16>().unwrap())
            .collect::<Vec<_>>();
        input.push(t);
    }
    let mut total = 1u32;
    for i in 0..input.get(0).unwrap().len() {
        let tt = input.get(0).unwrap().get(i).unwrap();
        let d: &u16 = input.get(1).unwrap().get(i).unwrap();

        let mut wins = 0u16;
        for t in 0..=*tt {
            if (tt - t) * t > *d {
                wins += 1;
            }
        }
        total *= wins as u32;
    }
    dbg!(total);
}

fn part_2() {
    let mut input: Vec<u64> = Vec::new();
    for l in include_str!("input.txt").split("\n") {
        let t = l
            .split_whitespace()
            .into_iter()
            .skip(1)
            .collect::<Vec<_>>()
            .join("");
        input.push(t.parse::<u64>().unwrap());
    }

    let mut wins_t = 0u64;
    let mut loss_t = 0u64;

    let tt = input.get(0).unwrap().clone();
    let d: u64 = input.get(1).unwrap().clone();

    let wins = ((tt as f32 - ((tt*tt - 4 *d ) as f32).sqrt()) / 2.0).ceil() as u32;
    let loss = ((tt as f32 + ((tt*tt - 4 *d ) as f32).sqrt()) / 2.0).floor() as u32;

    dbg!(loss - wins);
}

fn main() {
    bench(part_1);
    bench(part_2);
}
