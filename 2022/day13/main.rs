use std::fs;
use std::time;

use serde_json::Value;

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}
fn is_in_order(p1: &Value, p2: &Value) -> Option<bool> {
    if p1.is_number() && p2.is_number() {
        if p1.as_i64() <= p2.as_i64() {
            return None;
        } else {
            return Some(false);
        }
    } else if p1.is_number() {
        return is_in_order(&Value::Array(vec![p1.clone()]), p2);
    } else if p2.is_number() {
        return is_in_order(p1, &Value::Array(vec![p2.clone()]));
    } else {
        // both list
        for i in 0..*[p1.as_array().unwrap().len(), p2.as_array().unwrap().len()]
            .iter()
            .min()
            .unwrap()
        {
            let ret = is_in_order(&p1.as_array().unwrap()[i], &p2.as_array().unwrap()[i]);
            if ret.is_none() {
                continue;
            } else {
                return ret;
            }
        }

        if p1.as_array().unwrap().len() != p2.as_array().unwrap().len() {
            return Some(p1.as_array().unwrap().len() < p2.as_array().unwrap().len());
        }
    }

    assert!(false);
    return None;
}

fn part_1() {
    let input = fs::read_to_string("day13/test.txt")
        .unwrap()
        .split("\n\n")
        .map(|x| {
            x.split("\n")
                .map(|p| serde_json::from_str::<Value>(p).unwrap())
                .collect::<Vec<_>>()
        })
        .collect::<Vec<_>>();

    let mut idx = 0;
    let mut total = 0;

    for p in input {
        if is_in_order(&p[0], &p[1]).unwrap() {
            total += idx;
        }
        idx += 1;
    }

    println!("{}", total);
}

fn part_2() {
    let input = fs::read_to_string("test.txt")
        .unwrap()
        .split("\n\n")
        .map(|x| {
            x.split("\n")
                .map(|p| json::parse(p).unwrap())
                .collect::<Vec<_>>()
        })
        .collect::<Vec<_>>();
}

fn main() {
    bench(part_1);
    bench(part_2);
}
