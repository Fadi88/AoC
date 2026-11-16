use std::fmt::Display;
use std::time::Instant;

pub fn run_part<T: Display, F: FnOnce() -> T>(part_name: &str, func: F) {
    let start = Instant::now();
    let result = func();
    let duration = start.elapsed();
    println!("[{}] Result: {}", part_name, result);
    println!("[{}] Time: {:?}", part_name, duration);
}
