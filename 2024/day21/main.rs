use itertools::Itertools;
use std::collections::HashMap;
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

fn get_deltas(a: char, b: char, cache: &mut HashMap<(char, char), (i32, i32)>) -> (i32, i32) {
    if let Some(&result) = cache.get(&(a, b)) {
        return result;
    }

    let keypad = if "<>v^".chars().any(|c| a == c || b == c) {
        "X^A<v>"
    } else {
        "789456123X0A"
    };

    if a == b {
        return (0, 0);
    }

    let ax = (keypad.find(a).unwrap() % 3) as i32;
    let ay = (keypad.find(a).unwrap() / 3) as i32;
    let bx = (keypad.find(b).unwrap() % 3) as i32;
    let by = (keypad.find(b).unwrap() / 3) as i32;

    let result = (bx - ax, by - ay);
    cache.insert((a, b), result);
    result
}

fn is_valid_path(
    a: char,
    b: char,
    path: &str,
    cache: &mut HashMap<(char, char, String), bool>,
) -> bool {
    if let Some(&result) = cache.get(&(a, b, path.to_string())) {
        return result;
    }

    let keypad = if "<>v^".chars().any(|c| a == c || b == c) {
        "X^A<v>"
    } else {
        "789456123X0A"
    };

    let mut ax = (keypad.find(a).unwrap() % 3) as i32;
    let mut ay = (keypad.find(a).unwrap() / 3) as i32;

    let deltas = HashMap::from([('<', (-1, 0)), ('>', (1, 0)), ('v', (0, 1)), ('^', (0, -1))]);

    for p in path.chars() {
        if let Some(&(dx, dy)) = deltas.get(&p) {
            ax += dx;
            ay += dy;

            if ax < 0 || ax >= 3 || ay < 0 || ay >= (keypad.len() / 3) as i32 {
                cache.insert((a, b, path.to_string()), false);
                return false;
            }

            let idx = (ay * 3 + ax) as usize;
            if keypad.chars().nth(idx) == Some('X') {
                cache.insert((a, b, path.to_string()), false);
                return false;
            }
        }
    }

    cache.insert((a, b, path.to_string()), true);
    true
}
fn get_all_paths(a: char, b: char, cache: &mut HashMap<(char, char), Vec<String>>) -> Vec<String> {
    if let Some(result) = cache.get(&(a, b)) {
        return result.clone();
    }

    let (dx, dy) = get_deltas(a, b, &mut HashMap::new());

    let cx = if dx < 0 { "<" } else { ">" };
    let cy = if dy < 0 { "^" } else { "v" };

    let nx = format!(
        "{}{}",
        cx.repeat(dx.abs() as usize),
        cy.repeat(dy.abs() as usize)
    );

    let mut possible = Vec::new();

    for p in nx.chars().permutations(nx.len()) {
        let path: String = p.into_iter().collect();
        if is_valid_path(a, b, &path, &mut HashMap::new()) {
            possible.push(format!("{}A", path));
        }
    }

    cache.insert((a, b), possible.clone());

    possible
}

fn get_min_cost(
    seq: &str,
    depth: usize,
    cache: &mut HashMap<(String, usize), i32>,
    paths_cache: &mut HashMap<(char, char), Vec<String>>,
) -> i32 {
    if let Some(&result) = cache.get(&(seq.to_string(), depth)) {
        print!("cache hit , cost");
        return result;
    }

    let seq = format!("A{}", seq);

    let mut ret = 0;

    let chars: Vec<char> = seq.chars().collect();
    for i in 0..chars.len() - 1 {
        let a = chars[i];
        let b = chars[i + 1];

        let ps = get_all_paths(a, b, paths_cache);

        if depth == 0 {
            ret += ps.iter().map(|p| p.len()).min().unwrap() as i32;
        } else {
            ret += ps
                .iter()
                .map(|p| get_min_cost(p, depth - 1, cache, paths_cache))
                .min()
                .unwrap();
        }
    }

    cache.insert((seq, depth), ret);

    ret
}
fn part_1() {
    let seqs: Vec<&str> = include_str!("input.txt").lines().collect();

    let mut cost_cache: HashMap<(String, usize), i32> = HashMap::new();
    let mut paths_cache: HashMap<(char, char), Vec<String>> = HashMap::new();

    let mut t = 0;

    for seq in seqs {
        let cost = get_min_cost(seq, 2, &mut cost_cache, &mut paths_cache);
        let numeric_value: i32 = seq.replace("A", "").parse().unwrap();
        t += cost * numeric_value;
    }

    println!("{}", t);
}

fn part_2() {
    let seqs: Vec<&str> = include_str!("input.txt").lines().collect();

    let mut cost_cache: HashMap<(String, usize), i32> = HashMap::new();
    let mut paths_cache: HashMap<(char, char), Vec<String>> = HashMap::new();

    let mut t = 0;

    for seq in seqs {
        let cost = get_min_cost(seq, 15, &mut cost_cache, &mut paths_cache);
        let numeric_value: i32 = seq.replace("A", "").parse().unwrap();
        t += cost * numeric_value;
    }

    println!("{}", t);
}

fn main() {
    bench(part_1);
    bench(part_2);
}
