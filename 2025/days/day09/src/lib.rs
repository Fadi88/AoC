use anyhow::Result;
use itertools::Itertools;

type Tile = (i64, i64);
type Edge = (i64, i64, i64, i64);

fn parse_tiles(input: &str) -> Vec<Tile> {
    input
        .lines()
        .filter(|l| !l.is_empty())
        .map(|line| {
            let (x, y) = line.split_once(',').unwrap();
            (x.parse().unwrap(), y.parse().unwrap())
        })
        .collect()
}

fn get_normalized_edges(tiles: &[Tile]) -> Vec<Edge> {
    let mut edges = Vec::with_capacity(tiles.len());
    for i in 0..tiles.len() - 1 {
        let p1 = tiles[i];
        let p2 = tiles[i + 1];
        edges.push((
            p1.0.min(p2.0),
            p1.1.min(p2.1),
            p1.0.max(p2.0),
            p1.1.max(p2.1),
        ));
    }
    let p_last = tiles[tiles.len() - 1];
    let p_first = tiles[0];
    edges.push((
        p_last.0.min(p_first.0),
        p_last.1.min(p_first.1),
        p_last.0.max(p_first.0),
        p_last.1.max(p_first.1),
    ));
    edges
}

fn calculate_area(p1: Tile, p2: Tile) -> i64 {
    (p1.0 - p2.0).abs().saturating_add(1) * (p1.1 - p2.1).abs().saturating_add(1)
}

fn is_fully_contained(edges: &[Edge], min_x: i64, min_y: i64, max_x: i64, max_y: i64) -> bool {
    for &(e_min_x, e_min_y, e_max_x, e_max_y) in edges {
        if min_x < e_max_x && max_x > e_min_x && min_y < e_max_y && max_y > e_min_y {
            return false;
        }
    }
    true
}

pub fn part_1(input: &str) -> Result<String> {
    let tiles = parse_tiles(input);
    let max_area = tiles
        .iter()
        .tuple_combinations()
        .map(|(&p1, &p2)| calculate_area(p1, p2))
        .max()
        .unwrap_or(0);

    Ok(max_area.to_string())
}

pub fn part_2(input: &str) -> Result<String> {
    let tiles = parse_tiles(input);
    let edges = get_normalized_edges(&tiles);
    let mut result = 0;

    for (&p1, &p2) in tiles.iter().tuple_combinations() {
        let area = calculate_area(p1, p2);
        if area <= result {
            continue;
        }

        let (min_x, max_x) = if p1.0 < p2.0 {
            (p1.0, p2.0)
        } else {
            (p2.0, p1.0)
        };
        let (min_y, max_y) = if p1.1 < p2.1 {
            (p1.1, p2.1)
        } else {
            (p2.1, p1.1)
        };

        if is_fully_contained(&edges, min_x, min_y, max_x, max_y) {
            result = area;
        }
    }

    Ok(result.to_string())
}

#[cfg(test)]
mod tests {
    use super::*;

    const INPUT: &str = include_str!("../input.txt");

    #[test]
    fn test_part_1() {
        let result = part_1(INPUT).unwrap();
        println!("Part 1 result: {}", result);
        assert_eq!(result, "4764078684");
    }

    #[test]
    fn test_part_2() {
        let result = part_2(INPUT).unwrap();
        println!("Part 2 result: {}", result);
        assert_eq!(result, "1652344888");
    }
}
