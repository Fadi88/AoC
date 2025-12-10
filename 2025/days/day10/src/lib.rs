use anyhow::Result;
use minilp::{ComparisonOp, OptimizationDirection, Problem};
use nalgebra::{DMatrix, DVector};
use std::collections::{HashSet, VecDeque};
use std::fs;

#[derive(Debug, Clone)]
pub struct Machine {
    pub goal_mask: u32,
    pub goal_counters: Vec<i64>,
    pub button_masks: Vec<u32>,
}

pub fn parse(input: &str) -> Vec<Machine> {
    input
        .lines()
        .map(|line| {
            let parts: Vec<&str> = line.split_whitespace().collect();

            // 1. Goal Mask: <##.#>
            // Use slicing to match Python logic exactly
            let goal_str = &parts[0][1..parts[0].len() - 1];
            let mut goal_mask = 0;
            for (i, c) in goal_str.chars().enumerate() {
                if c == '#' {
                    goal_mask |= 1 << i;
                }
            }

            // 2. Goal Counters: {10,20,30}
            let last_part = parts.last().unwrap();
            let counter_str = &last_part[1..last_part.len() - 1];
            let goal_counters = counter_str
                .split(',')
                .map(|s| s.parse::<i64>().unwrap())
                .collect();

            // 3. Buttons: (1,2) or {3} or 4
            let mut button_masks = Vec::new();
            for part in &parts[1..parts.len() - 1] {
                let mut mask = 0;
                // Check for wrapping chars
                let inner = if part.starts_with('(') || part.starts_with('{') {
                    &part[1..part.len() - 1]
                } else {
                    part
                };

                for num_str in inner.split(',') {
                    if let Ok(bit) = num_str.parse::<u32>() {
                        mask |= 1 << bit;
                    }
                }
                button_masks.push(mask);
            }

            Machine {
                goal_mask,
                goal_counters,
                button_masks,
            }
        })
        .collect()
}

fn solve_bfs(machine: &Machine) -> i64 {
    let mut queue = VecDeque::new();
    queue.push_back((0u32, 0));
    let mut visited = HashSet::new();
    visited.insert(0);

    while let Some((curr, steps)) = queue.pop_front() {
        if curr == machine.goal_mask {
            return steps;
        }

        for &b_mask in &machine.button_masks {
            let nxt = curr ^ b_mask;
            if visited.insert(nxt) {
                queue.push_back((nxt, steps + 1));
            }
        }
    }
    0
}

fn solve_fast_path(
    matrix: &DMatrix<f64>,
    target: &DVector<f64>,
    num_buttons: usize,
) -> Option<i64> {
    let tol = 1e-5;

    let svd = matrix.clone().svd(true, true);
    let rank = svd.rank(tol);

    if rank == num_buttons {
        if let Ok(x) = svd.solve(target, tol) {
            let x_rounded: Vec<i64> = x.iter().map(|&v| v.round() as i64).collect();

            if x_rounded.iter().any(|&v| v < 0) {
                return None;
            }

            for (i, &v) in x.iter().enumerate() {
                if (v - x_rounded[i] as f64).abs() > tol {
                    return None;
                }
            }

            for r in 0..matrix.nrows() {
                let mut row_sum = 0.0;
                for c in 0..matrix.ncols() {
                    row_sum += matrix[(r, c)] * (x_rounded[c] as f64);
                }
                if (row_sum - target[r]).abs() > tol {
                    return None;
                }
            }

            return Some(x_rounded.iter().sum());
        }
    }
    None
}

fn solve_lp(machine: &Machine) -> i64 {
    let mut best_obj = i64::MAX;
    let mut stack = Vec::new();
    stack.push(Vec::<(usize, bool, f64)>::new());

    let mut iter_count = 0;
    while let Some(constraints) = stack.pop() {
        iter_count += 1;
        if iter_count > 2000 {
            break;
        }

        let mut problem = Problem::new(OptimizationDirection::Minimize);
        let vars: Vec<_> = (0..machine.button_masks.len())
            .map(|_| problem.add_var(1.0, (0.0, f64::INFINITY)))
            .collect();

        for i in 0..machine.goal_counters.len() {
            let mut row_coeffs = Vec::new();
            for (j, &b_mask) in machine.button_masks.iter().enumerate() {
                if (b_mask >> i) & 1 == 1 {
                    row_coeffs.push((vars[j], 1.0));
                }
            }
            problem.add_constraint(
                &row_coeffs,
                ComparisonOp::Eq,
                machine.goal_counters[i] as f64,
            );
        }

        for &(v_idx, is_le, val) in &constraints {
            if is_le {
                problem.add_constraint([(vars[v_idx], 1.0)], ComparisonOp::Le, val);
            } else {
                problem.add_constraint([(vars[v_idx], 1.0)], ComparisonOp::Ge, val);
            }
        }

        if let Ok(solution) = problem.solve() {
            let obj_val = solution.objective();

            if obj_val >= (best_obj as f64 - 1e-5) {
                continue;
            }

            let mut first_fractional = None;
            for (j, &v) in vars.iter().enumerate() {
                let val = solution[v];
                if (val - val.round()).abs() > 1e-4 {
                    first_fractional = Some((j, val));
                    break;
                }
            }

            match first_fractional {
                None => {
                    let current_int_sum = obj_val.round() as i64;
                    if current_int_sum < best_obj {
                        best_obj = current_int_sum;
                    }
                }
                Some((v_idx, val)) => {
                    let floor_val = val.floor();
                    let ceil_val = val.ceil();

                    let mut c1 = constraints.clone();
                    c1.push((v_idx, true, floor_val));
                    stack.push(c1);

                    let mut c2 = constraints.clone();
                    c2.push((v_idx, false, ceil_val));
                    stack.push(c2);
                }
            }
        }
    }

    if best_obj == i64::MAX {
        return 0;
    }
    best_obj
}

fn solve_p2(machine: &Machine) -> i64 {
    let num_goals = machine.goal_counters.len();
    let num_buttons = machine.button_masks.len();

    // Construct Matrix A and Vector b for fast path
    let mut elements = Vec::with_capacity(num_goals * num_buttons);
    for c in 0..num_buttons {
        for r in 0..num_goals {
            let val = if (machine.button_masks[c] >> r) & 1 == 1 {
                1.0
            } else {
                0.0
            };
            elements.push(val);
        }
    }
    // nalgebra is Column-Major! DMatrix::from_vec takes col-major data.
    // Our loops (c, then r) produce Column vectors sequentially. Correct.
    let matrix = DMatrix::from_vec(num_goals, num_buttons, elements);
    let target = DVector::from_vec(machine.goal_counters.iter().map(|&x| x as f64).collect());

    // Hyrid Approach
    if num_buttons <= num_goals {
        if let Some(res) = solve_fast_path(&matrix, &target, num_buttons) {
            return res;
        }
    }

    solve_lp(machine)
}

pub fn part_1() -> Result<String> {
    let input = fs::read_to_string("input.txt")?;
    let machines = parse(&input);
    let total: i64 = machines.iter().map(solve_bfs).sum();
    Ok(total.to_string())
}

pub fn part_2() -> Result<String> {
    let input = fs::read_to_string("input.txt")?;
    let machines = parse(&input);
    let total: i64 = machines.iter().map(solve_p2).sum();
    Ok(total.to_string())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_1() {
        println!("Part 1 result: {}", part_1().unwrap());
    }

    #[test]
    fn test_part_2() {
        println!("Part 2 result: {}", part_2().unwrap());
    }
}
