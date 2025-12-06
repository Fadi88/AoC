use anyhow::Result;

pub fn parse(input: &str) -> Vec<&str> {
    input.lines().collect()
}

pub fn part_1(input: &str) -> Result<String> {
    let parsed = parse(input);
    let ops = parsed
        .last()
        .unwrap()
        .split_whitespace()
        .collect::<Vec<&str>>();
    let rows = parsed
        .iter()
        .take(parsed.len() - 1)
        .map(|s| {
            s.split_whitespace()
                .map(|n| n.parse::<u16>().unwrap())
                .collect::<Vec<u16>>()
        })
        .collect::<Vec<Vec<u16>>>();

    let mut t: u64 = 0;
    for (idx, op) in ops.iter().enumerate() {
        if *op == "+" {
            t += rows.iter().map(|row| row[idx] as u64).sum::<u64>();
        } else if *op == "*" {
            t += rows.iter().map(|row| row[idx] as u64).product::<u64>();
        }
    }
    Ok(t.to_string())
}

fn calc_op<T: AsRef<str>>(op: &[T]) -> u64 {
    let first = op[0].as_ref();
    let operator = first.chars().last().unwrap();

    let first_num_str = &first[..first.len() - 1];
    let first_num = first_num_str.trim().parse::<u64>().unwrap_or(0);

    let rest_nums = op
        .iter()
        .skip(1)
        .filter_map(|s| s.as_ref().trim().parse::<u64>().ok());

    match operator {
        '+' => first_num + rest_nums.sum::<u64>(),
        '*' => first_num * rest_nums.product::<u64>(),
        _ => panic!("Invalid operator: {}", operator),
    }
}

pub fn part_2(input: &str) -> Result<String> {
    let lines: Vec<Vec<char>> = input.lines().map(|l| l.chars().collect()).collect();
    let width = lines.iter().map(|l| l.len()).max().unwrap_or(0);
    let height = lines.len();

    let mut total: u64 = 0;
    let mut current_group: Vec<String> = Vec::new();
    let mut col_buffer = String::with_capacity(height);

    for x in 0..width {
        col_buffer.clear();
        for row in &lines {
            col_buffer.push(row.get(x).copied().unwrap_or(' '));
        }

        let trimmed = col_buffer.trim();
        if trimmed.is_empty() {
            if !current_group.is_empty() {
                total += calc_op(&current_group);
                current_group.clear();
            }
        } else {
            current_group.push(trimmed.to_string());
        }
    }

    if !current_group.is_empty() {
        total += calc_op(&current_group);
    }

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
        assert!(!result.is_empty());
    }

    #[test]
    fn test_part_2() {
        let result = part_2(INPUT).unwrap();
        println!("Part 2 result: {}", result);
        assert!(!result.is_empty());
    }
}
