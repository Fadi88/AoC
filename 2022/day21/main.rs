use std::collections::HashMap;
use std::fs;
use std::time;
use regex::Regex;

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}
type Log = HashMap<String, String>;

fn get_value(monkeys: &Log, key: &str) -> i64 {
    match monkeys.get(key).unwrap().parse::<i64>() {
        Ok(x) => return x,
        Err(_) => {
            let p = monkeys.get(key).unwrap().split(" ").collect::<Vec<_>>();
            match p[1] {
                "+" => return get_value(monkeys, p[0]) + get_value(monkeys, p[2]),
                "-" => return get_value(monkeys, p[0]) - get_value(monkeys, p[2]),
                "*" => return get_value(monkeys, p[0]) * get_value(monkeys, p[2]),
                "/" => return get_value(monkeys, p[0]) / get_value(monkeys, p[2]),
                _ => -1,
            }
        }
    }
}

fn part_1() {
    let mut monkeys: Log = HashMap::new();
    for l in fs::read_to_string("input.txt").unwrap().lines() {
        let p = l.split(": ").collect::<Vec<_>>();

        monkeys.insert(p[0].to_string(), p[1].to_string());
    }

    println!("{}", get_value(&monkeys, "root"));
}

fn get_eq(monkeys: &Log, key: &str) -> String {
    if key.eq("humn") {
        return "humn".to_string();
    } else {
        match monkeys.get(key).unwrap().parse::<i64>() {
            Ok(x) => return x.to_string(),
            Err(_) => {
                let p = monkeys.get(key).unwrap().split(" ").collect::<Vec<_>>();

                let mut ret = "(".to_owned();
                ret += &get_eq(monkeys, p[0]);
                ret += if key == "root" { "=" } else { p[1] };
                ret += &get_eq(monkeys, p[2]);
                ret += ")";

                return ret;
            }
        }
    }
}

fn simplify(eq: &str) -> String {
    let mut ret = eq.clone();

    let re = Regex::new(r"\(-?\d+[+-/\*]-?\d+\)").unwrap();
    loop{
        let m = re.find_iter(ret).collect::<Vec<_>>();
        if m.len() == 0 {
            break
        }
        for par in m{
            let p = par.as_str();
        }
        break;
    }
    
    ret.to_string()
}

fn part_2() {
    let mut monkeys: Log = HashMap::new();
    for l in fs::read_to_string("input.txt").unwrap().lines() {
        let p = l.split(": ").collect::<Vec<_>>();

        monkeys.insert(p[0].to_string(), p[1].to_string());
    }

    let eq = simplify(&get_eq(&monkeys, "root"));
}

fn main() {
    bench(part_1);
    bench(part_2);
}
