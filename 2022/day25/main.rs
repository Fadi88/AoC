use std::fs;
use std::time;

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}

fn get_decimal(snafu: &str) -> i64 {
    let mut ret: i64 = 0;

    for (idx, c) in snafu.chars().rev().enumerate() {
        if c.is_numeric() {
            ret += c.to_digit(10).unwrap() as i64 * 5i64.pow(idx.try_into().unwrap());
        } else if c == '-' {
            ret -= 5i64.pow(idx.try_into().unwrap());
        } else if c == '=' {
            ret -= 2 * 5i64.pow(idx.try_into().unwrap());
        }
    }
    ret
}
fn get_snafu(mut n: i64) -> String {
    let mut ret: String = String::new();
    while n > 0 {
        let current_digit = n % 5;
        n /= 5;
        match current_digit {
            0..=2 => ret.push(char::from_digit(current_digit as u32, 10).unwrap()),
            3 => {
                ret.push('=');
            }
            4 => {
                ret.push('-');
            }
            _ => unreachable!(),
        }
    }
    ret
}
fn part_1() {
    println!(
        "{}",
        get_snafu(
            fs::read_to_string("input.txt")
                .unwrap()
                .lines()
                .map(|x| get_decimal(x))
                .sum::<i64>(),
        )
    );
}

fn main() {
    bench(part_1);
}
