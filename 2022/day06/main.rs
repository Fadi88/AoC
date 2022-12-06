use std::time;
use std::collections::HashSet;

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}

fn part_1() {
    let l = include_str!("input.txt").chars().collect::<Vec<_>>();

    let target_len = 4;

    for i in target_len-1..l.len(){

        let mut message :HashSet<char> = HashSet::new();

        for c in 0..target_len{
            message.insert(l[i-c]);
        }

        if message.len() == target_len{
            println!("{}" , i+1);
            break
        }

    }
}

fn part_2() {
    let l = include_str!("input.txt").chars().collect::<Vec<_>>();

    let target_len = 14;

    for i in target_len-1..l.len(){

        let mut message :HashSet<char> = HashSet::new();

        for c in 0..target_len{
            message.insert(l[i-c]);
        }

        if message.len() == target_len{
            println!("{}" , i+1);
            break
        }

    }
}

fn main() {
    bench(part_1);
    bench(part_2);
}
