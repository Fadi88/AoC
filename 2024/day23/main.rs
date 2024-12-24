use std::collections::{HashMap, HashSet};
use std::time::Instant;

fn bench<F, R>(f: F) -> R
where
    F: FnOnce() -> R,
{
    let t0 = Instant::now();
    let result = f(); // Call the function and store the result
    println!("time used: {:?}", Instant::now().duration_since(t0));
    result // Return the result of the function
}

fn part_1() {
    let input = include_str!("input.txt");

    let mut data: HashMap<&str, HashSet<&str>> = HashMap::new();
    for line in input.lines() {
        let parts: Vec<&str> = line.split('-').collect();
        if let [a, b] = parts[..] {
            data.entry(a).or_default().insert(b);
            data.entry(b).or_default().insert(a);
        }
    }

    let mut threes: HashSet<Vec<&str>> = HashSet::new();
    for (&key, neighbors) in &data {
        if key.starts_with('t') {
            let neighbors_vec: Vec<&str> = neighbors.iter().copied().collect();
            let n = neighbors_vec.len();
            for i in 0..n {
                for j in i + 1..n {
                    let c1 = neighbors_vec[i];
                    let c2 = neighbors_vec[j];
                    if data.get(c1).map_or(false, |neigh| neigh.contains(c2)) {
                        let mut triangle = vec![key, c1, c2];
                        triangle.sort_unstable();
                        threes.insert(triangle);
                    }
                }
            }
        }
    }

    println!("{}", threes.len());
}

fn bron_kerbosch<'a>(
    graph: &'a HashMap<&'a str, HashSet<&'a str>>,
    mut to_explore: HashSet<&'a str>,
    mut seen: HashSet<&'a str>,
    explored: HashSet<&'a str>,
) -> Vec<HashSet<&'a str>> {
    if to_explore.is_empty() && seen.is_empty() {
        return vec![explored];
    }

    let mut cliques = Vec::new();
    while let Some(&v) = to_explore.iter().next() {
        // Remove `v` from `to_explore`
        to_explore.remove(v);

        // Compute new sets for recursion
        let new_to_explore: HashSet<_> = to_explore.intersection(&graph[v]).copied().collect();
        let new_seen: HashSet<_> = seen.intersection(&graph[v]).copied().collect();
        let mut new_explored = explored.clone();
        new_explored.insert(v);

        // Recursive call
        cliques.extend(bron_kerbosch(graph, new_to_explore, new_seen, new_explored));

        // Add `v` to `seen`
        seen.insert(v);
    }

    cliques
}

fn part_2() {
    let input = include_str!("input.txt");

    // Parse the input into an adjacency list
    let mut data: HashMap<&str, HashSet<&str>> = HashMap::new();
    for line in input.lines() {
        let parts: Vec<&str> = line.split('-').collect();
        if let [a, b] = parts[..] {
            data.entry(a).or_default().insert(b);
            data.entry(b).or_default().insert(a);
        }
    }

    let cliques = bron_kerbosch(
        &data,
        data.keys().copied().collect(),
        HashSet::new(),
        HashSet::new(),
    );

    let mut sorted_cliques: Vec<_> = cliques.iter().collect();
    sorted_cliques.sort_by_key(|clique| (clique.len() as isize));

    if let Some(largest_clique) = sorted_cliques.last() {
        let mut largest_clique_vec: Vec<_> = largest_clique.iter().copied().collect();
        largest_clique_vec.sort();
        println!("{}", largest_clique_vec.join(","));
    }
}

fn main() {
    bench(part_1);
    bench(part_2);
}
