use std::collections::{BinaryHeap, HashMap, HashSet};
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


fn dijkstra(
    start: (i32, i32),
    free_spaces: &HashSet<(i32, i32)>,
) -> HashMap<((i32, i32), char), i32> {
    let deltas: HashMap<char, (i32, i32)> = HashMap::from([
        ('>', (1, 0)),
        ('v', (0, 1)),
        ('<', (-1, 0)),
        ('^', (0, -1)),
    ]);
    let rot = ['>', 'v', '<', '^'];

    let mut to_visit = BinaryHeap::new();
    let mut visited: HashMap<((i32, i32), char), i32> = HashMap::new();
    visited.insert((start, '>'), 0);

    to_visit.push((0, '>', start));

    while let Some((score, cd, (cx, cy))) = to_visit.pop() {
        let score = -score; // Negate score due to BinaryHeap being a min-heap

        if visited.get(&((cx, cy), cd)).map_or(false, |&v| v < score) {
            continue;
        }

        let (dx, dy) = deltas[&cd];

        // Try forward
        let np = (cx + dx, cy + dy);
        if free_spaces.contains(&np)
            && visited
                .get(&((np.0, np.1), cd))
                .map_or(true, |&v| v > score + 1)
        {
            visited.insert(((np.0, np.1), cd), score + 1);
            to_visit.push((-(score + 1), cd, np));
        }

        // Try turn
        for dr in [-1, 1] {
            let nd = rot[(((rot.iter().position(|&r| r == cd).unwrap() as i32) + dr + 4) % 4) as usize];
            if visited
                .get(&((cx, cy), nd))
                .map_or(true, |&v| v > score + 1000)
            {
                visited.insert(((cx, cy), nd), score + 1000);
                to_visit.push((-(score + 1000), nd, (cx, cy)));
            }
        }
    }

    visited
}


fn part_1() {
    let input_file = include_str!("input.txt");
    let mut start = (-1, -1);
    let mut end = (-1, -1);
    let mut free_spaces = HashSet::new();

    for (y, l) in input_file.lines().enumerate() {
        for (x, c) in l.chars().enumerate() {
            match c {
                'E' => {
                    end = (x as i32, y as i32);
                    free_spaces.insert((x as i32, y as i32));
                }
                'S' => {
                    start = (x as i32, y as i32);
                }
                '.' => {
                    free_spaces.insert((x as i32, y as i32));
                }
                _ => {}
            }
        }
    }

    let visited = dijkstra(start, &free_spaces);
    let min_score = visited
        .iter()
        .filter(|&(&(pos, _), _)| pos == end)
        .map(|(_, &score)| score)
        .min()
        .unwrap();

    println!("Part 1: {}", min_score);
}

fn trace_back(
    visited: &HashMap<((i32, i32), char), i32>,
    target_state: ((i32, i32), char),
) -> HashSet<(i32, i32)> {
    let deltas: HashMap<char, (i32, i32)> = HashMap::from([
        ('>', (1, 0)),
        ('v', (0, 1)),
        ('<', (-1, 0)),
        ('^', (0, -1)),
    ]);
    let rot = ['>', 'v', '<', '^'];

    let mut to_visit = vec![target_state];
    let mut seen = HashSet::new();

    while let Some((cp, cd)) = to_visit.pop() {
        seen.insert(cp);

        let (dx, dy) = deltas[&cd];
        let np = (cp.0 - dx, cp.1 - dy);

        // Try back forward
        if visited
            .get(&((np.0, np.1), cd))
            .map_or(false, |&v| v + 1 == visited[&((cp.0, cp.1), cd)])
        {
            to_visit.push(((np.0, np.1), cd));
        }

        // Try rotate
        let nd1 = rot[((rot.iter().position(|&r| r == cd).unwrap() as i32 + 1 + 4) % 4) as usize];
        let nd2 = rot[((rot.iter().position(|&r| r == cd).unwrap() as i32 - 1 + 4) % 4) as usize];

        if visited
            .get(&((cp.0, cp.1), nd1))
            .map_or(false, |&v| v + 1000 == visited[&((cp.0, cp.1), cd)])
        {
            to_visit.push(((cp.0, cp.1), nd1));
        }
        if visited
            .get(&((cp.0, cp.1), nd2))
            .map_or(false, |&v| v + 1000 == visited[&((cp.0, cp.1), cd)])
        {
            to_visit.push(((cp.0, cp.1), nd2));
        }
    }

    seen
}

fn part_2() {
    let input_file = include_str!("input.txt");
    let mut start = (-1, -1);
    let mut end = (-1, -1);
    let mut free_spaces = HashSet::new();

    for (y, l) in input_file.lines().enumerate() {
        for (x, c) in l.chars().enumerate() {
            match c {
                'E' => {
                    end = (x as i32, y as i32);
                    free_spaces.insert((x as i32, y as i32));
                }
                'S' => {
                    start = (x as i32, y as i32);
                }
                '.' => {
                    free_spaces.insert((x as i32, y as i32));
                }
                _ => {}
            }
        }
    }

    let visited = dijkstra(start, &free_spaces);

    let target_score = visited
        .iter()
        .filter(|&(&(pos, _), _)| pos == end)
        .map(|(_, &score)| score)
        .min()
        .unwrap();

    let target_state = visited
        .iter()
        .find(|&(&(pos, _), &score)| pos == end && score == target_score)
        .map(|(&(pos, dir), _)| (pos, dir))
        .unwrap();

    let path_len = trace_back(&visited, target_state).len();
    println!("Part 2: {}", path_len);
}

fn main() {
    bench(part_1);
    bench(part_2);
}
