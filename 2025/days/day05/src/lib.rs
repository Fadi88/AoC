use anyhow::Result;
#[allow(unused_imports)]
use itertools::Itertools;

pub fn parse(input: &str) -> Vec<&str> {
    input.lines().collect()
}

/// Parse input sections, normalizing line endings
fn parse_sections(input: &str) -> Vec<String> {
    input
        .replace("\r\n", "\n")
        .split("\n\n")
        .map(|s| s.to_string())
        .collect()
}

fn parse_range(line: &str) -> (i64, i64) {
    let parts: Vec<&str> = line.split('-').collect();
    let a: i64 = parts[0].trim().parse().unwrap();
    let b: i64 = parts[1].trim().parse().unwrap();
    (a, b)
}

fn parse_ranges(section: &str) -> Vec<(i64, i64)> {
    let mut ranges: Vec<(i64, i64)> = section.lines().map(parse_range).collect();
    ranges.sort();
    ranges
}

fn merge_ranges(ranges: &[(i64, i64)]) -> Vec<(i64, i64)> {
    if ranges.is_empty() {
        return vec![];
    }

    let mut merged: Vec<(i64, i64)> = vec![ranges[0]];
    for &(start, end) in &ranges[1..] {
        let last_idx = merged.len() - 1;
        if merged[last_idx].1 >= start {
            merged[last_idx].1 = merged[last_idx].1.max(end);
        } else {
            merged.push((start, end));
        }
    }
    merged
}

fn parse_values(section: &str) -> Vec<i64> {
    section.lines().map(|s| s.trim().parse().unwrap()).collect()
}

fn in_range(ranges: &[(i64, i64)], x: i64) -> bool {
    let mut left = 0;
    let mut right = ranges.len() - 1;
    let mut idx = None;

    while left <= right {
        let mid = (left + right) / 2;
        if ranges[mid].0 <= x {
            idx = Some(mid);
            left = mid + 1;
        } else {
            if mid == 0 {
                break;
            }
            right = mid - 1;
        }
    }

    if let Some(i) = idx {
        ranges[i].0 <= x && x <= ranges[i].1
    } else {
        false
    }
}

pub fn part_1(input: &str) -> Result<String> {
    let sections = parse_sections(input);
    let ranges = parse_ranges(&sections[0]);
    let merged = merge_ranges(&ranges);
    let values = parse_values(&sections[1]);

    let count = values.iter().filter(|&&x| in_range(&merged, x)).count();

    Ok(count.to_string())
}

pub fn part_2(input: &str) -> Result<String> {
    let sections = parse_sections(input);
    let ranges = parse_ranges(&sections[0]);
    let merged = merge_ranges(&ranges);

    let total: u64 = merged
        .iter()
        .fold(0, |acc, (s, e)| acc + (e - s + 1) as u64);

    Ok(total.to_string())
}

#[cfg(test)]
mod tests {
    use super::*;

    const INPUT: &str = include_str!("../input.txt");

    #[test]
    fn test_part_1() {
        let result = part_1(INPUT).unwrap();
        println!("Part 1 result: {}", result);
        assert_eq!(result, "782");
    }

    #[test]
    fn test_part_2() {
        let result = part_2(INPUT).unwrap();
        println!("Part 2 result: {}", result);
        assert!(!result.is_empty());
    }
}
