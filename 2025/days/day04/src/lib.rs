use anyhow::Result;
#[allow(unused_imports)]
use itertools::Itertools;

use std::collections::HashSet;

pub fn parse(input: &str) -> HashSet<(i32, i32)> {
    let mut paper = HashSet::new();
    for (y, line) in input.lines().enumerate() {
        for (x, c) in line.chars().enumerate() {
            if c == '@' {
                paper.insert((x as i32, y as i32));
            }
        }
    }
    paper
}

fn count_neighbors(x: i32, y: i32, paper: &HashSet<(i32, i32)>) -> usize {
    let mut count = 0;
    for dx in -1..=1 {
        for dy in -1..=1 {
            if dx == 0 && dy == 0 {
                continue;
            }
            if paper.contains(&(x + dx, y + dy)) {
                count += 1;
            }
        }
    }
    count
}

pub fn part_1(input: &str) -> Result<String> {
    let paper = parse(input);
    let count = paper
        .iter()
        .filter(|&&(x, y)| count_neighbors(x, y, &paper) < 4)
        .count();
    Ok(count.to_string())
}

pub fn part_2(input: &str) -> Result<String> {
    let mut paper = parse(input);
    let original_size = paper.len();

    loop {
        let to_remove: Vec<_> = paper
            .iter()
            .filter(|&&(x, y)| count_neighbors(x, y, &paper) < 4)
            .cloned()
            .collect();

        if to_remove.is_empty() {
            break;
        }

        for pos in to_remove {
            paper.remove(&pos);
        }
    }

    Ok((original_size - paper.len()).to_string())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_1() {
        let input = std::fs::read_to_string("input.txt").unwrap();
        assert_eq!(part_1(&input).unwrap(), "1451");
    }

    #[test]
    fn test_part_2() {
        let input = std::fs::read_to_string("input.txt").unwrap();
        assert_eq!(part_2(&input).unwrap(), "8701");
    }
}
