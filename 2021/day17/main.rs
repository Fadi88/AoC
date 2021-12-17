use regex::Regex;
use std::time;

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}

fn part_1() {
    let l = include_str!("input.txt");
    let re = Regex::new(r".*=-?\d+\.+-?\d+.*=(-?\d+)..-?\d+").unwrap();

    let nums = re.captures(l).unwrap();

    let y1: i16 = nums[1].parse().unwrap();

    println!(
        "part 1 : {:?}",
        (y1.abs() as u32 * (y1.abs() - 1) as u32) / 2
    );
}

fn get_pos(vx0: i32, vy0: i32, t: i32) -> (i32, i32) {
    let y = vy0 * t - (t - 1) * (t) / 2;
    let x = if t < vx0 {
        (2 * vx0 - t + 1) * (t) / 2
    } else {
        (vx0 * (vx0 + 1) / 2) as i32
    };
    (x, y)
}
fn will_intersect(v: (i32, i32), u: (i32, i32), l: (i32, i32)) -> bool {
    let tmin = (((v.1 * v.1 - 2 * u.1) as f32).sqrt() + v.1 as f32).floor() as i32;
    let tmax = (((v.1 * v.1 - 2 * l.1) as f32).sqrt() + v.1 as f32).floor() as i32;

    for t in tmin..=tmax + 1 {
        let (x, y) = get_pos(v.0, v.1, t);
        if x >= u.0 && x <= l.0 && y >= l.1 && y <= u.1 {
            return true;
        }
    }

    return false;
}

fn part_2() {
    let l = include_str!("input.txt");
    let re = Regex::new(r".*=(-?\d+)\.+(-?\d+).*=(-?\d+)..(-?\d+)").unwrap();

    let nums = re.captures(l).unwrap();

    let x1: i32 = nums[1].parse().unwrap();
    let x2: i32 = nums[2].parse().unwrap();
    let y1: i32 = nums[3].parse().unwrap();
    let y2: i32 = nums[4].parse().unwrap();

    let vy_min = y1;
    let vx_max = x2;

    let vy_max = -y1;
    let vx_min = ((2.0 * x1 as f32).sqrt() - 1.0).floor() as i32;

    let upper_bound = (x1, y2);
    let lower_bound = (x2, y1);

    let mut cnt: u16 = 0;
    for vx in vx_min..=vx_max {
        for vy in vy_min..=vy_max {
            if will_intersect((vx, vy), upper_bound, lower_bound) {
                cnt += 1;
            }
        }
    }

    println!("part 2 : {:?}", cnt);
}

fn main() {
    bench(part_1);
    bench(part_2);
}
