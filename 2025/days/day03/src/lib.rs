use anyhow::Result;
#[allow(unused_imports)]
use itertools::Itertools;
use std::cmp::max;

pub fn parse() -> Vec<Vec<u8>> {
    let input = include_str!("../input.txt");
    input
        .lines()
        .map(|line| {
            line.trim()
                .chars()
                .map(|c| c.to_digit(10).unwrap() as u8)
                .collect()
        })
        .collect()
}

pub fn get_max_val(data: &Vec<u8>) -> u64 {
    let mut max_val = 0;
    let mut max_seen = data[data.len() - 1];
    for x in data.iter().rev().skip(1) {
        max_val = max(max_val, 10 * x + max_seen);
        max_seen = max(max_seen, *x);
    }
    max_val.into()
}

pub fn part_1() -> Result<String> {
    let parsed = parse();
    Ok(parsed
        .iter()
        .map(|x| get_max_val(x))
        .sum::<u64>()
        .to_string())
}

pub fn get_max_12(data: &Vec<u8>) -> u64 {
    let n = data.len();
    let mut result: u64 = 0;
    let mut current_idx = 0;

    for k in (1..=12).rev() {
        let search_end = n - k + 1;
        let window = &data[current_idx..search_end];
        let max_d = window.iter().max().unwrap();

        // Find the first occurrence of max_d in the window
        let offset = window.iter().position(|&x| x == *max_d).unwrap();

        result = result * 10 + (*max_d as u64);
        current_idx += offset + 1;
    }
    result
}

pub fn part_2() -> Result<String> {
    let parsed = parse();
    // TODO: Solve Part 2
    Ok(parsed
        .iter()
        .map(|x| get_max_12(x))
        .sum::<u64>()
        .to_string())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_1() {
        assert_eq!(part_1().unwrap(), "16973");
    }

    #[test]
    fn test_part_2() {
        assert_eq!(part_2().unwrap(), "168027167146027");
    }
}
