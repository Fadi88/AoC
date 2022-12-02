use std::collections::HashMap;
use std::time;

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}

fn part_1() {
    let mut freq: HashMap<&str, u16> = HashMap::new();
    for l in include_str!("input.txt").split("\n") {
        *freq.entry(l).or_default() += 1;
    }

    let mut score: u16 = 0;
    for k in freq {
        let hands: Vec<_> = k.0.split(' ').collect();

        let h0 = hands[0].chars().next().unwrap() as u16 - 'A' as u16;
        let h1 = hands[1].chars().next().unwrap() as u16 - 'X' as u16;

        // game score = value of hand(R1,P2,S3) + 3*(L0,T1,W2)
        let g_score = (h1 + 1) + (3 * (((h1 as i8 - h0 as i8) + 4) % 3)) as u16;

        score += (g_score as u16 * k.1) as u16;
    }

    println!("{}", score);
}

fn part_2() {
    let mut freq: HashMap<&str, u16> = HashMap::new();
    for l in include_str!("input.txt").split("\n") {
        *freq.entry(l).or_default() += 1;
    }

    let mut score: u16 = 0;
    for k in freq {
        let hands: Vec<_> = k.0.split(' ').collect();

        let h0 = hands[0].chars().next().unwrap() as u16 - 'A' as u16;
        let h1 = hands[1].chars().next().unwrap() as u16 - 'X' as u16;

        let g_score = h1 * 3 + (h0 as i8 + h1 as i8 +3 -1) as u16 % 3 + 1 ;

        score += g_score * k.1;
    }

    println!("{}", score);
}

fn main() {
    bench(part_1);
    bench(part_2);
}
