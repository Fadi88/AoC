use std::fs;
use std::time;

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}

fn get_taxi_distance(p1: &(i32, i32), p2: &(i32, i32)) -> u32 {
    p1.0.abs_diff(p2.0) + p1.1.abs_diff(p2.1)
}

fn part_1() {
    let mut grid: Vec<((i32, i32), (i32, i32))> = Vec::new();
    for l in fs::read_to_string("input.txt").unwrap().split("\n") {
        let ls = l
            .replace("Sensor at ", "")
            .replace(" closest beacon is at ", "")
            .replace(" ", "")
            .replace(":", ",")
            .replace("x=", "")
            .replace("y=", "");
        let mut ps = ls.split(",").map(|x| x.parse::<i32>().unwrap());

        grid.push((
            (ps.next().unwrap(), ps.next().unwrap()),
            (ps.next().unwrap(), ps.next().unwrap()),
        ))
    }

    let mut confirmed_free: Vec<(i32, i32)> = Vec::new();
    let target_y = 2000000;

    for (sensor, beacon) in grid {
        let b_s_dst = get_taxi_distance(&sensor, &beacon);
        let dy = sensor.1.abs_diff(target_y);

        if dy <= b_s_dst {
            let dx = (b_s_dst - dy) as i32;
            confirmed_free.push((sensor.0 - dx, sensor.0 + dx));
        }
    }
    confirmed_free.sort();

    let mut combined_ranges: Vec<(i32, i32)> = Vec::new();

    combined_ranges.push(confirmed_free[0]);

    for i in 1..confirmed_free.len() {
        let r = confirmed_free[i];
        let to_check = combined_ranges.last().unwrap();

        if r.0 > to_check.1 {
            combined_ranges.push(r);
        } else {
            *combined_ranges.last_mut().unwrap() =
                (to_check.0, [r.1, to_check.1].iter().max().unwrap().clone());
        }
    }

    let mut total: u32 = 0;
    for r in combined_ranges {
        total += (r.1 - r.0) as u32;
    }

    println!("{}", total);
}

fn part_2() {
    let mut grid: Vec<((i32, i32), (i32, i32))> = Vec::new();

    for l in fs::read_to_string("input.txt").unwrap().split("\n") {
        let ls = l
            .replace("Sensor at ", "")
            .replace(" closest beacon is at ", "")
            .replace(" ", "")
            .replace(":", ",")
            .replace("x=", "")
            .replace("y=", "");
        let mut ps = ls.split(",").map(|x| x.parse::<i32>().unwrap());

        grid.push((
            (ps.next().unwrap(), ps.next().unwrap()),
            (ps.next().unwrap(), ps.next().unwrap()),
        ))
    }

    for y in 0..4000000 {
        let mut free_xs: Vec<(i32, i32)> = Vec::new();

        for (sensor, beacon) in &grid {
            let b_s_dst = get_taxi_distance(&sensor, &beacon);
            let dy = sensor.1.abs_diff(y);

            if dy < b_s_dst {
                let dx = (b_s_dst - dy) as i32;
                free_xs.push((
                    [sensor.0 - dx, 0].iter().max().unwrap().clone(),
                    [sensor.0 + dx, 4000000].iter().min().unwrap().clone(),
                ));
            }
        }

        free_xs.sort();
        let mut combined_ranges: Vec<(i32, i32)> = Vec::new();

        combined_ranges.push(free_xs[0]);

        for i in 1..free_xs.len() {
            let r = free_xs[i];
            let to_check = combined_ranges.last().unwrap();

            if r.0 > to_check.1 {
                combined_ranges.push(r);
            } else {
                *combined_ranges.last_mut().unwrap() =
                    (to_check.0, [r.1, to_check.1].iter().max().unwrap().clone());
            }
        }

        // assert that the whole range is covered
        assert!(combined_ranges.first().unwrap().0 == 0);
        assert!(combined_ranges.last().unwrap().1 == 4000000);

        if combined_ranges.len() > 1 {
            println!(
                "{}",
                4000000u64 * (combined_ranges.first().unwrap().1 + 1) as u64 + y as u64
            );
        }
    }
}

fn main() {
    bench(part_1);
    bench(part_2);
}
