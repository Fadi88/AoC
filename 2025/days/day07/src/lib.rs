use anyhow::Result;

pub struct Parsed {
    grid: Vec<Vec<bool>>,
    start_x: usize,
    start_y: usize,
    width: usize,
    last_splitter_y: usize,
}

pub fn parse(input: &str) -> Parsed {
    let lines: Vec<&str> = input.lines().collect();
    let raw_height = lines.len();
    let raw_width = lines.first().map(|l| l.len()).unwrap_or(0);

    let width = raw_width + 2;
    let mut grid = vec![vec![false; width]; raw_height];
    let mut s = (0, 0);
    let mut last_splitter_y = 0;

    for (y, line) in lines.iter().enumerate() {
        for (x, c) in line.chars().enumerate() {
            if c == '^' {
                grid[y][x + 1] = true;
                if y > last_splitter_y {
                    last_splitter_y = y;
                }
            } else if c == 'S' {
                s = (x + 1, y);
            }
        }
    }

    Parsed {
        grid,
        start_x: s.0,
        start_y: s.1,
        width,
        last_splitter_y,
    }
}

pub fn part_1(input: &str) -> Result<String> {
    let data = parse(input);
    let mut tips = vec![false; data.width];

    tips[data.start_x] = true;

    let mut total_splits = 0;

    for y in (data.start_y + 1)..=data.last_splitter_y {
        let mut next_tips = vec![false; data.width];

        for x in 1..data.width - 1 {
            if tips[x] {
                if data.grid[y][x] {
                    total_splits += 1;
                    next_tips[x - 1] = true;
                    next_tips[x + 1] = true;
                } else {
                    next_tips[x] = true;
                }
            }
        }
        tips = next_tips;
    }

    Ok(total_splits.to_string())
}

pub fn part_2(input: &str) -> Result<String> {
    let data = parse(input);
    let mut tips = vec![0usize; data.width];

    tips[data.start_x] = 1;

    let mut total_timelines = 1;

    for y in (data.start_y + 1)..=data.last_splitter_y {
        let mut next_tips = vec![0usize; data.width];

        for x in 1..data.width - 1 {
            let count = tips[x];
            if count > 0 {
                if data.grid[y][x] {
                    total_timelines += count;
                    next_tips[x - 1] += count;
                    next_tips[x + 1] += count;
                } else {
                    next_tips[x] += count;
                }
            }
        }
        tips = next_tips;
    }

    Ok(total_timelines.to_string())
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
