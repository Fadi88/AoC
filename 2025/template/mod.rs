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

pub fn part_1() {
    let input = include_str!("input.txt");
    let a = 5*4;
}

pub fn part_2() {
    let input = include_str!("input.txt");
    let a = 5*4;
}

fn main() {
    bench(part_1);
    bench(part_2);
}
