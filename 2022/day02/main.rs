use std::time;

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}

fn part_1() {
    let mut cals : Vec<u32> =Vec::new();
    for l in include_str!("input.txt").split("\n\n"){
        let temp = l.split("\n").map(|x| x.parse::<u32>().unwrap()).sum();
        cals.push(temp);
    }
    cals.sort();

    println!("{}" , cals.iter().last().unwrap());
}

fn part_2() {
    let mut cals : Vec<u32> =Vec::new();
    for l in include_str!("input.txt").split("\n\n"){
        let temp = l.split("\n").map(|x| x.parse::<u32>().unwrap()).sum();
        cals.push(temp);
    }
    cals.sort();

    println!("{}" , cals.iter().rev().take(3).sum::<u32>());
}

fn main() {
    bench(part_1);
    bench(part_2);
}
