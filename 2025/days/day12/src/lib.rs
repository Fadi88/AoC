use anyhow::Result;
use std::fs;

type Shape = (u128, usize);

pub fn parse(input: &str) -> (Vec<Shape>, Vec<String>) {
    let input = input.replace("\r\n", "\n");
    let chunks: Vec<&str> = input.split("\n\n").collect();

    if chunks.is_empty() {
        return (vec![], vec![]);
    }

    let shape_chunks = &chunks[..chunks.len() - 1];
    let region_chunk = chunks[chunks.len() - 1];

    let mut shapes = Vec::new();
    for chunk in shape_chunks {
        let lines: Vec<&str> = chunk.lines().collect();
        if lines.len() > 1 {
            let shape_lines = lines[1..].join("");
            let flattened = shape_lines.replace('\n', "");

            let area = flattened.chars().filter(|&c| c == '#').count();

            let mut mask: u128 = 0;
            for c in flattened.chars() {
                mask <<= 1;
                if c == '#' {
                    mask |= 1;
                }
            }
            shapes.push((mask, area));
        }
    }

    let region_lines = region_chunk.lines().map(|s| s.to_string()).collect();

    (shapes, region_lines)
}

fn is_region_valid(region: &str, shapes: &[Shape]) -> bool {
    if let Some((dims, reqs)) = region.split_once(": ") {
        if let Some((w_str, h_str)) = dims.split_once('x') {
            let width: usize = w_str.parse().unwrap();
            let height: usize = h_str.parse().unwrap();
            let available_area = width * height;

            let required_counts: Vec<usize> = reqs
                .split_whitespace()
                .map(|s| s.parse().unwrap_or(0))
                .collect();

            let mut required_area = 0;
            for (idx, &count) in required_counts.iter().enumerate() {
                if idx < shapes.len() {
                    required_area += count * shapes[idx].1;
                }
            }

            return available_area >= required_area;
        }
    }
    false
}

pub fn part_1() -> Result<String> {
    let input = fs::read_to_string("input.txt")?;
    let (shapes, region_lines) = parse(&input);

    let count = region_lines
        .iter()
        .filter(|line| is_region_valid(line, &shapes))
        .count();

    Ok(count.to_string())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_1() {
        let result = part_1().unwrap();
        assert_eq!(result, "448");
    }
}
