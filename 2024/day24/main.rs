use regex::Regex;
use std::collections::HashMap;
use std::collections::HashSet;
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

fn get_num(d: &HashMap<&str, i64>, c: &str) -> i64 {
    let re = Regex::new(&format!(r"{}[0-9]+", c)).unwrap();
    let mut top = 0;
    for i in d.keys() {
        if re.is_match(i) {
            let num = i[c.len()..].parse::<i64>().unwrap();
            top = top.max(num);
        }
    }

    let mut ret = String::new();
    for i in (0..=top).rev() {
        let key = format!("{}{:02}", c, i);
        match d.get(&key as &str) {
            Some(&val) => ret.push_str(&val.to_string()),
            None => return -1,
        }
    }
    i64::from_str_radix(&ret, 2).unwrap()
}

fn get_value(
    op: &str,
    wires: &HashMap<&str, i64>,
    xs: &HashMap<&str, i64>,
    ys: &HashMap<&str, i64>,
) -> Option<i64> {
    if op.starts_with('x') {
        xs.get(op).copied()
    } else if op.starts_with('y') {
        ys.get(op).copied()
    } else if let Ok(val) = op.parse::<i64>() {
        Some(val)
    } else {
        wires.get(op).copied()
    }
}

fn eval_loop(
    res: &HashMap<&str, (&str, &str, &str)>,
    xs: &HashMap<&str, i64>,
    ys: &HashMap<&str, i64>,
) -> i64 {
    let mut wires: HashMap<&str, i64> = HashMap::new();
    while wires.len() < res.len() {
        for (d, &(op0, op1, op2)) in res {
            let v1 = get_value(op0, &wires, xs, ys);
            let v2 = get_value(op2, &wires, xs, ys);

            if let (Some(v1), Some(v2)) = (v1, v2) {
                let result = match op1 {
                    "AND" => v1 & v2,
                    "OR" => v1 | v2,
                    "XOR" => v1 ^ v2,
                    _ => panic!("Unknown operation: {}", op1),
                };
                wires.insert(d, result);
            }
        }
    }
    get_num(&wires, "z")
}
fn part_1() {
    let input = include_str!("input.txt");
    let data: Vec<&str> = input.split("\n\n").collect();
    let mut xs = HashMap::new();
    let mut ys = HashMap::new();
    for l in data[0].lines() {
        let (key, value) = l.split_once(':').unwrap();
        let value = value.trim().parse::<i64>().unwrap();
        if key.contains('x') {
            xs.insert(key, value);
        } else {
            ys.insert(key, value);
        }
    }

    let mut res = HashMap::new();
    for l in data[1].lines() {
        let parts: Vec<&str> = l.split_whitespace().collect();
        assert!(parts.len() == 5);
        res.insert(parts[4], (parts[0], parts[1], parts[2]));
    }

    println!("{}", eval_loop(&res, &xs, &ys));
}

fn part_2() {
    let input = include_str!("input.txt");
    let data: Vec<&str> = input.split("\n\n").collect();
    let mut xs = HashMap::new();
    let mut ys = HashMap::new();
    for l in data[0].lines() {
        let (key, value) = l.split_once(':').unwrap();
        let value = value.trim().parse::<i64>().unwrap();
        if key.contains('x') {
            xs.insert(key, value);
        } else {
            ys.insert(key, value);
        }
    }

    let mut ops: HashMap<&str, (&str, &str, &str)> = HashMap::new();
    let mut rev_ops: HashMap<(&str, &str, &str), &str> = HashMap::new();

    for l in data[1].lines() {
        let parts: Vec<&str> = l.split_whitespace().collect();
        assert!(parts.len() == 5);
        ops.insert(parts[4], (parts[0], parts[1], parts[2]));

        rev_ops.insert((parts[0], parts[1], parts[2]), parts[4]);
        rev_ops.insert((parts[2], parts[1], parts[0]), parts[4]);
    }

    let re = Regex::new(r"z\d+").unwrap();
    let mut top = 0;
    for d in ops.keys() {
        if re.is_match(d) {
            let num = d[1..].parse::<i64>().unwrap();
            top = top.max(num);
        }
    }

    let mut wrong_gates: HashSet<String> = HashSet::new();

    for i in 1..top {
        let x = format!("x{:02}", i);
        let y = format!("y{:02}", i);
        let z = format!("z{:02}", i);

        let res_op = ops.get(&z as &str).unwrap();

        let xor_gate = rev_ops.get(&(x.as_str(), "XOR", y.as_str())).unwrap();
        let and_gate = rev_ops.get(&(x.as_str(), "AND", y.as_str())).unwrap();

        if !res_op.1.contains("XOR") {
            wrong_gates.insert(z.to_string());
        }

        let mut carry = Vec::new();
        for (o0, o1, o2) in ops.values() {
            if o1 == &"XOR" && (o0 == xor_gate || o2 == xor_gate) {
                let mut set = HashSet::from([o0, o1, o2]);
                set.remove(&"XOR");
                set.remove(xor_gate);
                carry.push(set);
            }
        }

        if carry.len() != 1 {
            wrong_gates.insert(xor_gate.to_string());
            wrong_gates.insert(and_gate.to_string());
        } else {
            let carry = carry[0].iter().next().unwrap();
            let xor2_gate = rev_ops.get(&(xor_gate, "XOR", carry)).unwrap();
            if xor2_gate != &z {
                wrong_gates.insert(xor2_gate.to_string());
            }
        }
    }

    let mut wrong_gates: Vec<String> = wrong_gates.into_iter().collect();
    wrong_gates.sort();
    println!("{}", wrong_gates.join(","));
}

fn main() {
    bench(part_1);
    bench(part_2);
}
