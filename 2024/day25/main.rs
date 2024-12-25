use std::iter::zip;
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

fn get_heights(d: &[&str]) -> Vec<usize> {
    let mut ret = Vec::new();
    let width = d[0].len();

    for i in 0..width {
        let count = d
            .iter()
            .filter(|line| line.chars().nth(i) == Some('#'))
            .count();
        ret.push(count);
    }
    ret
}

fn does_fit(p: (&[usize], &[usize])) -> bool {
    let (k, l) = p;
    zip(k, l).all(|(ki, li)| ki + li <= 7)
}
fn part_1() {
    let input_file = include_str!("input.txt"); // Include the file at compile time
    let mut key_heights = Vec::new();
    let mut lock_heights = Vec::new();

    for block in input_file.split("\n\n") {
        let lines: Vec<&str> = block.lines().collect();
        if lines[0].contains('.') {
            lock_heights.push(get_heights(&lines));
        } else {
            key_heights.push(get_heights(&lines));
        }
    }

    let mut s = 0;
    for key in &key_heights {
        for lock in &lock_heights {
            if does_fit((key, lock)) {
                s += 1;
            }
        }
    }

    println!("{}", s);
}

fn main() {
    bench(part_1);
}
