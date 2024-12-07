use itertools::Itertools;
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

fn eval_right_to_left(nums: &Vec<i64>, target: i64, ops: &Vec<&&str>) -> bool {
    let mut s = nums[0];
    for i in 0..ops.len() {
        match *ops[i] {
            "+" => s += nums[i + 1],
            "*" => s *= nums[i + 1],
            "||" => {
                let digits = (nums[i + 1] as f64).log10().floor() as i64 + 1;
                s = (s * 10i64.pow(digits as u32) + nums[i + 1]) as i64;
            }
            _ => panic!("Invalid operator"),
        }
        if s > target {
            return false;
        }
    }
    s == target
}

fn does_match(target: i64, nums: &Vec<i64>, ops: &Vec<&str>) -> bool {
    for op_vec in std::iter::repeat(ops.iter())
        .take(nums.len() - 1)
        .multi_cartesian_product()
    {
        if eval_right_to_left(nums, target, &op_vec) {
            return true;
        }
    }
    false
}
fn part_1() {
    let contents = include_str!("input.txt");
    let cals: Vec<(i64, Vec<i64>)> = contents
        .lines()
        .map(|l| {
            let ps: Vec<&str> = l.trim().split(':').collect();
            let v = ps[0].parse::<i64>().unwrap();
            let nums: Vec<i64> = ps[1]
                .split_whitespace()
                .map(|s| s.parse::<i64>().unwrap())
                .collect();
            (v, nums)
        })
        .collect();

    let sum: i64 = cals
        .iter()
        .filter(|&(v, nums)| does_match(*v, nums, &vec!["+", "*"]))
        .map(|&(v, _)| v)
        .sum();

    println!("{}", sum);
}

fn part_2() {
    let contents = include_str!("input.txt");
    let cals: Vec<(i64, Vec<i64>)> = contents
        .lines()
        .map(|l| {
            let ps: Vec<&str> = l.trim().split(':').collect();
            let v = ps[0].parse::<i64>().unwrap();
            let nums: Vec<i64> = ps[1]
                .split_whitespace()
                .map(|s| s.parse::<i64>().unwrap())
                .collect();
            (v, nums)
        })
        .collect();

    let sum: i64 = cals
        .iter()
        .filter(|&(v, nums)| does_match(*v, nums, &vec!["+", "*", "||"]))
        .map(|&(v, _)| v)
        .sum();

    println!("{}", sum);
}

fn main() {
    bench(part_1);
    bench(part_2);
}
