use std::collections::HashSet;
use std::time;

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}

fn sim_cycle(cycles: u8) -> u16 {
    let mut input = include_str!("input.txt").split("\n\n");

    let algo = input.next().unwrap().chars().collect::<Vec<_>>();

    let img: Vec<_> = input.next().unwrap().split("\n").collect();

    let mut lit_pix: HashSet<(i16, i16)> = HashSet::new();
    for (y, l) in img.iter().enumerate() {
        for (x, c) in l.chars().enumerate() {
            if c == '#' {
                lit_pix.insert((x as i16, y as i16));
            }
        }
    }

    for iter in 0..cycles {
        let mut new_pix: HashSet<(i16, i16)> = HashSet::new();
        let xs = lit_pix.iter().map(|x| x.0).collect::<Vec<_>>();
        let ys = lit_pix.iter().map(|x| x.1).collect::<Vec<_>>();

        let (x_l, x_u) = (xs.iter().min().unwrap(), xs.iter().max().unwrap());
        let (y_l, y_u) = (ys.iter().min().unwrap(), ys.iter().max().unwrap());

        for x in (x_l - 1)..(x_u + 2) {
            for y in (y_l - 1)..(y_u + 2) {
                let mut idx: String = String::from("");

                for t in 0..9 {
                    let nx = x + t % 3 - 1;
                    let ny = y + t / 3 - 1;

                    if (x_l..=x_u).contains(&&nx) && (y_l..=y_u).contains(&&ny) {
                        idx += if lit_pix.contains(&(nx, ny)) {
                            "1"
                        } else {
                            "0"
                        };
                    } else {
                        idx += if iter % 2 == 1 { "1" } else { "0" };
                    }
                }

                if algo[usize::from_str_radix(&idx, 2).unwrap()] == '#' {
                    new_pix.insert((x, y));
                }
            }
        }

        lit_pix = new_pix;
    }

    lit_pix.len() as u16
}

fn part_1() {
    println!("part 1 : {}", sim_cycle(2));
}

fn part_2() {
    println!("part 2 : {}", sim_cycle(50));
}

fn main() {
    bench(part_1);
    bench(part_2);
}
