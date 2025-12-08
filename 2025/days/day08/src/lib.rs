use anyhow::{Ok, Result};
use std::cmp::Reverse;
use std::collections::{BinaryHeap, HashSet};

#[derive(Debug, Clone, Copy)]
struct Point(i64, i64, i64);

fn parse(input: &str) -> Vec<Point> {
    input
        .lines()
        .filter(|l| !l.trim().is_empty())
        .map(|line| {
            let parts: Vec<i64> = line.split(',').map(|s| s.trim().parse().unwrap()).collect();
            Point(parts[0], parts[1], parts[2])
        })
        .collect()
}

fn dist_sq(p1: &Point, p2: &Point) -> i64 {
    (p1.0 - p2.0).pow(2) + (p1.1 - p2.1).pow(2) + (p1.2 - p2.2).pow(2)
}

fn get_pairs(points: &[Point]) -> Vec<(i64, usize, usize)> {
    let mut pairs = Vec::with_capacity(points.len() * (points.len() - 1) / 2);
    for i in 0..points.len() {
        for j in (i + 1)..points.len() {
            pairs.push((dist_sq(&points[i], &points[j]), i, j));
        }
    }
    pairs
}

pub fn part_1(input: &str) -> Result<String> {
    let points = parse(input);
    let mut pairs = get_pairs(&points);

    pairs.sort_unstable_by_key(|k| k.0);
    let top_pairs = &pairs[..1000.min(pairs.len())];

    let mut components: Vec<HashSet<usize>> = (0..points.len())
        .map(|i| {
            let mut s = HashSet::new();
            s.insert(i);
            s
        })
        .collect();

    for &(_d, i, j) in top_pairs {
        let mut idx_i = None;
        let mut idx_j = None;

        for (idx, comp) in components.iter().enumerate() {
            if comp.contains(&i) {
                idx_i = Some(idx);
            }
            if comp.contains(&j) {
                idx_j = Some(idx);
            }
        }

        if let (Some(ii), Some(jj)) = (idx_i, idx_j) {
            if ii != jj {
                let other = components[jj].clone();
                components[ii].extend(other);
                components.remove(jj);
            }
        }
    }

    let mut sizes: Vec<_> = components.iter().map(|c| c.len()).collect();
    sizes.sort_unstable_by(|a, b| b.cmp(a));

    while sizes.len() < 3 {
        sizes.push(0);
    }

    Ok((sizes[0] * sizes[1] * sizes[2]).to_string())
}

pub fn part_2(input: &str) -> Result<String> {
    let points = parse(input);
    let pairs = get_pairs(&points);

    let mut heap = BinaryHeap::new();
    for p in pairs {
        heap.push(Reverse(p));
    }

    let mut components: Vec<HashSet<usize>> = (0..points.len())
        .map(|i| {
            let mut s = HashSet::new();
            s.insert(i);
            s
        })
        .collect();

    while let Some(Reverse((_, i, j))) = heap.pop() {
        let mut idx_i = None;
        let mut idx_j = None;

        for (idx, comp) in components.iter().enumerate() {
            if comp.contains(&i) {
                idx_i = Some(idx);
            }
            if comp.contains(&j) {
                idx_j = Some(idx);
            }
        }

        if let (Some(ii), Some(jj)) = (idx_i, idx_j) {
            if ii != jj {
                let other = components[jj].clone();
                components[ii].extend(other);
                components.remove(jj);

                if components.len() == 1 {
                    let p1 = points[i];
                    let p2 = points[j];
                    return Ok((p1.0 * p2.0).to_string());
                }
            }
        }
    }

    Ok("0".to_string())
}
