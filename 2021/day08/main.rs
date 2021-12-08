use std::collections::HashSet;
use std::time;

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}

fn part_1() {
    let mut cnt = 0;
    for l in include_str!("input.txt").split("\n") {
        let patterns = l.split(" | ").collect::<Vec<_>>();

        for pat in patterns[1].split(" ") {
            if [2, 3, 4, 7].contains(&pat.len()) {
                cnt += 1;
            }
        }
    }

    println!("part 1 : {}", cnt);
}

fn part_2() {
    let mut total = 0;
    for l in include_str!("./input.txt").split("\n") {
        let patterns = l.split(" | ").collect::<Vec<_>>();

        let mut mapping: [HashSet<char>; 10] = Default::default();

        for pat in patterns[0].split(" ") {
            match pat.len() {
                2 => mapping[1] = pat.chars().into_iter().collect(),
                3 => mapping[7] = pat.chars().into_iter().collect(),
                4 => mapping[4] = pat.chars().into_iter().collect(),
                7 => mapping[8] = pat.chars().into_iter().collect(),
                _ => (),
            }
        }

        for pat in patterns[0].split(" ") {
            if pat.len() == 5 {
                let tmp: HashSet<char> = pat.chars().into_iter().collect();

                if mapping[1].difference(&tmp).count() == 0 {
                    mapping[3] = tmp;
                } else if tmp.difference(&mapping[4]).count() == 2 {
                    mapping[5] = tmp;
                } else if tmp.difference(&mapping[4]).count() == 3 {
                    mapping[2] = tmp;
                }
            }
        }

        for pat in patterns[0].split(" ") {
            if pat.len() == 6 {
                let tmp: HashSet<char> = pat.chars().into_iter().collect();

                if mapping[1].difference(&tmp).count() == 1 {
                    mapping[6] = tmp;
                } else if mapping[5].difference(&tmp).count() == 0 {
                    mapping[9] = tmp;
                } else {
                    mapping[0] = tmp;
                }
            }
        }

        let mut num = 0;
        for (i, pat) in patterns[1]
            .split(" ")
            .collect::<Vec<_>>()
            .iter()
            .rev()
            .enumerate()
        {
            let tmp: HashSet<char> = pat.chars().into_iter().collect();
            num += mapping.iter().position(|x| x == &tmp).unwrap() as i32 * i32::pow(10, i as u32);
        }
        total += num;
    }

    println!("part 2 : {}", total);
}
fn main() {
    bench(part_1);
    bench(part_2);
}
