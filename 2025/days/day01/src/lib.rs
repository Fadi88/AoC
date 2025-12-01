use anyhow::Result;

pub fn parse(input: &str) -> Vec<&str> {
    input.split_whitespace().collect()
}

pub fn part_1(input: &str) -> Result<String> {
    let data = parse(input);
    let mut p: i32 = 50;
    let mut zeros = 0;

    for r in data {
        let dir_char = r.chars().next().unwrap();
        let amt: i32 = r[1..].parse()?;
        let direction = match dir_char {
            'R' => 1,
            'L' => -1,
            _ => panic!("Invalid direction"),
        };

        p = (p + direction * amt).rem_euclid(100);
        if p == 0 {
            zeros += 1;
        }
    }
    Ok(zeros.to_string())
}

pub fn part_2(input: &str) -> Result<String> {
    let data = parse(input);
    let mut p: i32 = 50;
    let mut zeros = 0;

    for r in data {
        let dir_char = r.chars().next().unwrap();
        let amt: i32 = r[1..].parse()?;
        let direction = match dir_char {
            'R' => 1,
            'L' => -1,
            _ => panic!("Invalid direction"),
        };

        zeros += amt / 100;
        let remainder = amt % 100;

        let new_p = p + direction * remainder;

        if direction == 1 {
            zeros += (new_p >= 100) as i32;
        } else {
            zeros += (new_p <= 0 && p != 0) as i32;
        }

        p = new_p.rem_euclid(100);
    }
    Ok(zeros.to_string())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_1() {
        // Add test cases if needed
    }

    #[test]
    fn test_part_2() {
        // Add test cases if needed
    }
}
