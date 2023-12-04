use std::collections::{HashMap, HashSet};
use std::time;

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}

fn part_1() {
    let mut total = 0u16;

    for l in include_str!("input.txt").split("\n") {
        let ticket = l
            .split(":")
            .nth(1)
            .unwrap()
            .split("|")
            .map(|s| s.split_whitespace().collect::<HashSet<_>>())
            .collect::<Vec<_>>();
        
        let cnt =ticket
                .get(0)
                .unwrap()
                .intersection(ticket.get(1).unwrap())
                .count();
        if cnt > 0{
            total += 2u16.pow(cnt as u32 -1 );
        }

    }

    dbg!(total);
}

fn part_2() {
    let mut ticket_count: HashMap<u16, u32> = HashMap::new();

    for (card, l) in include_str!("input.txt").split("\n").enumerate() {
        *ticket_count.entry(card as u16 + 1).or_insert(0) += 1;

        let ticket = l
            .split(":")
            .nth(1)
            .unwrap()
            .split("|")
            .map(|s| s.split_whitespace().collect::<HashSet<_>>())
            .collect::<Vec<_>>();

        let cnt = ticket
            .get(0)
            .unwrap()
            .intersection(ticket.get(1).unwrap())
            .count();

        for n in 0..cnt {
            let num = ticket_count.get(&(card as u16 + 1)).unwrap().clone();
            *ticket_count.entry(card as u16 + 2 + n as u16).or_insert(0) += num;
        }
    }
    dbg!(ticket_count.values().sum::<u32>());
}

fn main() {
    bench(part_1);
    bench(part_2);
}
