use anyhow::Result;

pub fn parse(input: &str) -> Vec<(u64, u64)> {
    input
        .trim()
        .split(',')
        .map(|s| {
            let (start, end) = s.split_once('-').expect("Invalid format");
            (start.parse().unwrap(), end.parse().unwrap())
        })
        .collect()
}

fn is_invalid_id(num: u64) -> bool {
    let s = num.to_string();
    let len = s.len();
    if !len.is_multiple_of(2) {
        return false;
    }
    let mid = len / 2;
    s[..mid] == s[mid..]
}

pub fn part_1(input: &str) -> Result<String> {
    let data = parse(input);
    let mut s = 0;
    for (start, end) in data {
        for num in start..=end {
            if is_invalid_id(num) {
                s += num;
            }
        }
    }
    Ok(s.to_string())
}

pub fn part_2(input: &str) -> Result<String> {
    let data = parse(input);
    let mut s = 0;
    for (start, end) in data {
        for num in start..=end {
            if is_invalid_2_opt(num) {
                s += num;
            }
        }
    }
    Ok(s.to_string())
}

fn gcd(mut a: usize, mut b: usize) -> usize {
    while b != 0 {
        let t = b;
        b = a % b;
        a = t;
    }
    a
}

fn is_invalid_2_opt(num: u64) -> bool {
    let s = num.to_string();
    let l = s.len();
    let first_char = s.chars().next().unwrap();
    let ff = s.chars().filter(|&c| c == first_char).count();

    let common = gcd(l, ff);

    if common < 2 {
        return false;
    }

    for k in (2..=common).rev() {
        if common.is_multiple_of(k) {
            let d = l / k;
            // Check if s == s[:d] * k
            let sub = &s[..d];
            if s == sub.repeat(k) {
                return true;
            }
        }
    }
    false
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_1() {
        let input = std::fs::read_to_string("input.txt").unwrap();
        assert_eq!(part_1(&input).unwrap(), "23560874270");
    }

    #[test]
    fn test_part_2() {
        let input = std::fs::read_to_string("input.txt").unwrap();
        assert_eq!(part_2(&input).unwrap(), "44143124633");
    }
}
