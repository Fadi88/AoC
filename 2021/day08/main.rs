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
    for l in include_str!("input.txt").split("\n") {
        let patterns = l.split(" | ").collect::<Vec<_>>();

        for pat in patterns[0].split(" ") {

        }
    }

    println!("part 2 : {}", total);
}

fn main() {
    bench(part_1);
    bench(part_2);
}
