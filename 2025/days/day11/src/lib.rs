use anyhow::Result;
use std::collections::HashMap;
use std::fs;

// Adjacency list: node -> list of neighbors
type Graph<'a> = HashMap<&'a str, Vec<&'a str>>;

pub fn parse(input: &str) -> Graph<'_> {
    let mut grid: Graph = HashMap::new();
    for line in input.lines() {
        let parts: Vec<&str> = line.split(": ").collect();
        let key = parts[0];
        let neighbors: Vec<&str> = parts[1].split_whitespace().collect();
        grid.entry(key).or_default().extend(neighbors);
    }
    grid
}

fn count_paths<'a>(
    curr: &'a str,
    target: &'a str,
    graph: &Graph<'a>,
    memo: &mut HashMap<(&'a str, &'a str), u64>,
) -> u64 {
    if curr == target {
        return 1;
    }
    let key = (curr, target);
    if let Some(&count) = memo.get(&key) {
        return count;
    }

    let mut total = 0;
    if let Some(neighbors) = graph.get(curr) {
        for &nxt in neighbors {
            total += count_paths(nxt, target, graph, memo);
        }
    }

    memo.insert(key, total);
    total
}

pub fn part_1() -> Result<String> {
    let input = fs::read_to_string("input.txt")?;
    let grid = parse(&input);
    let mut memo = HashMap::new();
    let result = count_paths("you", "out", &grid, &mut memo);
    Ok(result.to_string())
}

pub fn part_2() -> Result<String> {
    let input = fs::read_to_string("input.txt")?;
    let grid = parse(&input);
    let mut memo = HashMap::new();

    let p1 = count_paths("svr", "dac", &grid, &mut memo)
        * count_paths("dac", "fft", &grid, &mut memo)
        * count_paths("fft", "out", &grid, &mut memo);

    let p2 = count_paths("svr", "fft", &grid, &mut memo)
        * count_paths("fft", "dac", &grid, &mut memo)
        * count_paths("dac", "out", &grid, &mut memo);

    Ok((p1 + p2).to_string())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_1() {
        let result = part_1().unwrap();
        println!("Part 1 result: {}", result);
        assert!(!result.is_empty());
    }

    #[test]
    fn test_part_2() {
        let result = part_2().unwrap();
        println!("Part 2 result: {}", result);
        assert!(!result.is_empty());
    }
}
