use std::fs;
use std::time;

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}
#[derive(Debug)]
enum Operand {
    Val(u64),
    Old,
}
#[derive(Debug)]
struct Monkey {
    items: Vec<u64>,
    operation: (char, Operand),
    test: u8,
    if_true: usize,
    if_false: usize,
    activity: u32,
}

impl Monkey {
    pub fn new(m: &str) -> Monkey {
        let mut items: Vec<u64> = Vec::new();
        let mut operation = ('x', Operand::Old);
        let mut if_true: usize = 0;
        let mut if_false: usize = 0;
        let mut test: u8 = 0;

        for l in m.split("\n") {
            if l.contains("Starting items: ") {
                items.append(
                    &mut l
                        .trim_start()
                        .replace("Starting items: ", "")
                        .replace(",", "")
                        .split(" ")
                        .map(|x| x.parse::<u64>().unwrap())
                        .collect(),
                );
            } else if l.contains("Operation:") {
                let p = l.split(" ").collect::<Vec<_>>();
                let op = p
                    .get(p.len().wrapping_sub(2))
                    .unwrap()
                    .chars()
                    .next()
                    .unwrap();

                let val = p.get(p.len().wrapping_sub(1)).unwrap();

                if val.contains("old") {
                    operation = (op, Operand::Old);
                } else {
                    operation = (op, Operand::Val(val.parse::<u64>().unwrap()));
                }
            } else if l.contains("Test:") {
                test = l.split(" ").last().unwrap().parse().unwrap();
            } else if l.contains("If true:") {
                if_true = l.split(" ").last().unwrap().parse().unwrap();
            } else if l.contains("If false:") {
                if_false = l.split(" ").last().unwrap().parse().unwrap();
            }
        }
        return Monkey {
            items: items,
            operation: operation,
            test: test,
            if_true: if_true,
            if_false: if_false,
            activity: 0,
        };
    }

    pub fn round(&mut self) -> Vec<(usize, u64)> {
        let mut ret: Vec<(usize, u64)> = Vec::new();

        for i in &self.items {
            self.activity += 1;

            let mut tmp: u64 = match &self.operation.1 {
                Operand::Val(x) => *x,
                Operand::Old => *i,
            };

            if self.operation.0 == '+' {
                tmp += *i;
            } else if self.operation.0 == '*' {
                tmp *= i;
            }
            tmp /= 3;
            ret.push((
                if tmp % self.test as u64 == 0 {
                    self.if_true
                } else {
                    self.if_false
                },
                tmp,
            ));
        }
        self.items.clear();
        ret
    }

    pub fn round_2(&mut self) -> Vec<(usize, u64)> {
        let mut ret: Vec<(usize, u64)> = Vec::new();

        for i in &self.items {
            self.activity += 1;

            let mut tmp: u64 = match &self.operation.1 {
                Operand::Val(x) => *x,
                Operand::Old => *i,
            };

            if self.operation.0 == '+' {
                tmp += *i;
            } else if self.operation.0 == '*' {
                tmp *= i;
            }
            ret.push((
                if tmp % self.test as u64 == 0 {
                    self.if_true
                } else {
                    self.if_false
                },
                tmp,
            ));
        }
        self.items.clear();
        ret
    }
}

fn part_1() {
    let mut monkeys: Vec<Monkey> = Vec::new();

    for m in fs::read_to_string("input.txt").unwrap().split("\n\n") {
        monkeys.push(Monkey::new(m))
    }
    for _ in 0..20 {
        for i in 0..monkeys.len() {
            let tmp = monkeys[i].round();
            for t in tmp {
                monkeys[t.0].items.push(t.1);
            }
        }
    }

    monkeys.sort_by(|a, b| b.activity.cmp(&a.activity));
    println!("{}", monkeys[0].activity * monkeys[1].activity);
}
fn part_2() {
    let mut monkeys: Vec<Monkey> = Vec::new();

    for m in fs::read_to_string("input.txt").unwrap().split("\n\n") {
        monkeys.push(Monkey::new(m))
    }
    let mut divisor: u64 = 1;
    for m in &monkeys {
        divisor *= m.test as u64;
    }

    for _ in 0..10000 {
        for i in 0..monkeys.len() {
            let tmp = monkeys[i].round_2();
            for t in tmp {
                monkeys[t.0].items.push(t.1 % divisor);
            }
        }
    }

    monkeys.sort_by(|a, b| b.activity.cmp(&a.activity));
    println!(
        "{}",
        monkeys[0].activity as u64 * monkeys[1].activity as u64
    );
}
fn main() {
    bench(part_1);
    bench(part_2);
}
