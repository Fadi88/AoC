use std::collections::VecDeque;
use std::time::Instant;

fn bench<F, R>(f: F) -> R
where
    F: FnOnce() -> R,
{
    let t0 = Instant::now();
    let result = f(); // Call the function and store the result
    println!("time used: {:?}", Instant::now().duration_since(t0));
    result // Return the result of the function
}

fn exec(prog: &[usize], mut reg: [usize; 3]) -> Vec<String> {
    let mut pc = 0;
    let mut output = Vec::new();

    while pc <= prog.len() - 2 {
        let op = prog[pc];
        let opreand = prog[pc + 1];
        assert!(0 <= opreand && opreand < 7);
        let combo = if opreand < 4 {
            opreand
        } else {
            reg[opreand - 4]
        };

        match op {
            0 => {
                // adv
                reg[0] /= 2usize.pow(combo as u32);
            }
            1 => {
                // bxl
                reg[1] ^= opreand;
            }
            2 => {
                // bst
                reg[1] = combo % 8;
            }
            3 => {
                // jnz
                if reg[0] != 0 {
                    pc = opreand;
                    continue;
                }
            }
            4 => {
                // bxl
                reg[1] ^= reg[2];
            }
            5 => {
                output.push((combo % 8).to_string());
            }
            6 => {
                // bdv
                reg[1] = reg[0] / 2usize.pow(combo as u32);
            }
            7 => {
                // cdv
                reg[2] = reg[0] / 2usize.pow(combo as u32);
            }
            _ => panic!("Invalid opcode"),
        }

        pc += 2;
    }

    output
}

fn part_1() {
    let input_file = include_str!("input.txt");
    let ps: Vec<&str> = input_file.split("\n\n").collect();

    let reg: [usize; 3] = ps[0]
        .lines()
        .map(|l| l.split(':').nth(1).unwrap().trim().parse().unwrap())
        .collect::<Vec<usize>>()
        .try_into()
        .unwrap();

    let prog: Vec<usize> = ps[1]
        .split(':')
        .nth(1)
        .unwrap()
        .split(',')
        .map(|s| s.trim().parse().unwrap())
        .collect();

    let output = exec(&prog, reg);
    println!("{}", output.join(","));
}

fn part_2() {
    let input_file = include_str!("input.txt");
    let ps: Vec<&str> = input_file.split("\n\n").collect();

    let prog: Vec<usize> = ps[1]
        .split(':')
        .nth(1)
        .unwrap()
        .split(',')
        .map(|s| s.trim().parse().unwrap())
        .collect();

    let mut to_visit = VecDeque::from([(prog.len(), 0)]);

    while let Some((pos, a)) = to_visit.pop_front() {
        for i in 0..8 {
            let n_a = a * 8 + i;
            let o = exec(&prog, [n_a, 0, 0]);
            if o.iter()
                .map(|a| a.parse::<usize>().unwrap())
                .collect::<Vec<_>>()
                == prog[pos - 1..]
            {
                to_visit.push_back((pos - 1, n_a));
                if o.len() == prog.len() {
                    println!("{}", n_a);
                    return;
                }
            }
        }
    }
}

fn main() {
    bench(part_1);
    bench(part_2);
}
