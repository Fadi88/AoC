use std::collections::HashMap;
use std::time;

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}

fn shoe_lace(poly: Vec<(i64, i64)>) -> i64 {
    let mut ret: i64 = 0;
    for i in 0..poly.len() {
        let c_p = poly.get(i).unwrap();
        let p_p = poly
            .get(if i == 0 { poly.len() - 1 } else { i - 1 })
            .unwrap();

        ret += p_p.0 * c_p.1 - p_p.1 * c_p.0;
    }
    ret / 2 as i64
}

fn part_1() {
    let mut poly: Vec<(i64, i64)> = vec![(0, 0)];

    let deltas: HashMap<char, (i64, i64)> =
        HashMap::from([('R', (1, 0)), ('L', (-1, 0)), ('D', (0, 1)), ('U', (0, -1))]);

    let mut pt_cnt = 0i64;

    for l in include_str!("input.txt").split("\n") {
        let p = l.split(' ').collect::<Vec<_>>();
        let lp = poly.last().unwrap();
        let d = deltas
            .get(&p.get(0).unwrap().chars().nth(0).unwrap())
            .unwrap();
        let steps = p.get(1).unwrap().parse::<i64>().unwrap();
        pt_cnt += steps as i64;
        poly.push((lp.0 + d.0 * steps, lp.1 + d.1 * steps));
    }

    dbg!(shoe_lace(poly) + pt_cnt / 2 + 1);
}

fn part_2() {
    let mut poly: Vec<(i64, i64)> = vec![(0, 0)];

    let deltas: HashMap<char, (i64, i64)> =
        HashMap::from([('0', (1, 0)), ('2', (-1, 0)), ('1', (0, 1)), ('3', (0, -1))]);

    let mut pt_cnt = 0i64;

    for l in include_str!("input.txt").split("\n") {
        let p = l.split(' ').collect::<Vec<_>>();
        let lp = poly.last().unwrap();

        let code = p.get(2).unwrap();
        let steps = i64::from_str_radix(code.get(2..code.len() - 2).unwrap(), 16).unwrap();

        let d = deltas
            .get(&code.get(0..code.len() - 1).unwrap().chars().last().unwrap())
            .unwrap();

        pt_cnt += steps as i64;
        poly.push((lp.0 + d.0 * steps, lp.1 + d.1 * steps));
    }

    dbg!(shoe_lace(poly) + pt_cnt / 2 + 1);
}

fn main() {
    bench(part_1);
    bench(part_2);
}
