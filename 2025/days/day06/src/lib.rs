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

    #[test]
    fn test_part_1() {
        let input = "test input";
        assert_eq!(part_1(input).unwrap(), "10");
    }

    #[test]
    fn test_part_2() {
        let input = "test input";
        assert_eq!(part_2(input).unwrap(), "10");
    }
}
