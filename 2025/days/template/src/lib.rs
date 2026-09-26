use anyhow::Result;
#[allow(unused_imports)]
use itertools::Itertools;

pub fn parse(input: &str) -> Vec<&str> {
    input.lines().collect()
}

pub fn part_1(input: &str) -> Result<String> {
    let _parsed = parse(input);
    // TODO: Solve Part 1
    Ok(input.len().to_string())
}

pub fn part_2(input: &str) -> Result<String> {
    let _parsed = parse(input);
    // TODO: Solve Part 2
    Ok(input.len().to_string())
}

#[cfg(test)]
mod tests {
    use super::*;

    fn input() -> String {
        std::fs::read_to_string(concat!(env!("CARGO_MANIFEST_DIR"), "/input.txt")).unwrap()
    }

    #[test]
    fn test_part_1() {
        let result = part_1(&input()).unwrap();
        println!("Part 1 result: {}", result);
        assert!(!result.is_empty());
    }

    #[test]
    fn test_part_2() {
        let result = part_2(&input()).unwrap();
        println!("Part 2 result: {}", result);
        assert!(!result.is_empty());
    }
}
