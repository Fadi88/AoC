use std::collections::{HashMap, HashSet};
use std::time;

type Beacon = [i16; 3];

fn bench<T>(f: fn() -> T ) -> T  {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}
fn distance(p1: &Beacon, p2: &Beacon) -> u16 {
    let dx = (p1[0] - p2[0]) as i32;
    let dy = (p1[1] - p2[1]) as i32;
    let dz = (p1[2] - p2[2]) as i32;

    ((dx * dx + dy * dy + dz * dz) as f32).sqrt() as u16
}

fn distance_taxi(p1: &Beacon, p2: &Beacon) -> u16 {
    let dx = (p1[0] - p2[0]) as i32;
    let dy = (p1[1] - p2[1]) as i32;
    let dz = (p1[2] - p2[2]) as i32;

    (dx.abs() + dy.abs() + dz.abs()) as u16
}

fn get_config(scanner: &HashSet<Beacon>) -> HashMap<Beacon, HashSet<u16>> {
    let mut config: HashMap<Beacon, HashSet<u16>> = HashMap::new();

    for p1 in scanner {
        for p2 in scanner {
            if p1 == p2 {
                continue;
            }
            (config.entry(p1.clone()).or_insert(HashSet::new()))
                .insert(distance(&p1, &p2));
        }
    }
    config
}

fn get_common_pt_num(
    s1: &HashMap<Beacon, HashSet<u16>>,
    s2: &HashMap<Beacon, HashSet<u16>>,
) -> u16 {
    let mut commons: Vec<u16> = Vec::new();
    for p1 in s1.keys() {
        for p2 in s2.keys() {
            commons.push(
                s1.get(p1)
                    .unwrap()
                    .intersection(s2.get(p2).unwrap())
                    .count() as u16,
            );
        }
    }

    *commons.iter().max().unwrap()
}

fn allign(
    config1: &HashMap<Beacon, HashSet<u16>>,
    config2: &HashMap<Beacon, HashSet<u16>>,
) -> ([i16; 3], HashMap<u8, (u8, i8)>) {
    let mut mapping: HashMap<Beacon, Beacon> = HashMap::new();
    for p1 in config1.keys() {
        for p2 in config2.keys() {
            if config1
                .get(p1)
                .unwrap()
                .intersection(config2.get(p2).unwrap())
                .count()
                > 10
            {
                mapping.insert(*p1, *p2);
            }
        }
    }

    let cog_1_x = mapping
        .keys()
        .map(|x| x[0] as i32)
        .collect::<Vec<_>>()
        .iter()
        .sum::<i32>() as f32
        / mapping.keys().count() as f32;

    let cog_1_y = mapping
        .keys()
        .map(|x| x[1] as i32)
        .collect::<Vec<_>>()
        .iter()
        .sum::<i32>() as f32
        / mapping.keys().count() as f32;

    let cog_1_z = mapping
        .keys()
        .map(|x| x[2] as i32)
        .collect::<Vec<_>>()
        .iter()
        .sum::<i32>() as f32
        / mapping.keys().count() as f32;

    let cog_2_x = mapping
        .values()
        .map(|x| x[0] as i32)
        .collect::<Vec<_>>()
        .iter()
        .sum::<i32>() as f32
        / mapping.keys().count() as f32;

    let cog_2_y = mapping
        .values()
        .map(|x| x[1] as i32)
        .collect::<Vec<_>>()
        .iter()
        .sum::<i32>() as f32
        / mapping.keys().count() as f32;

    let cog_2_z = mapping
        .values()
        .map(|x| x[2] as i32)
        .collect::<Vec<_>>()
        .iter()
        .sum::<i32>() as f32
        / mapping.keys().count() as f32;

    let p1 = mapping.keys().last().unwrap();
    let p2 = mapping.get(p1).unwrap();

    let p1_mod = [
        (p1[0] as f32 - cog_1_x).round() as i16,
        (p1[1] as f32 - cog_1_y).round() as i16,
        (p1[2] as f32 - cog_1_z).round() as i16,
    ];

    let p2_mod = [
        (p2[0] as f32 - cog_2_x).round() as i16,
        (p2[1] as f32 - cog_2_y).round() as i16,
        (p2[2] as f32 - cog_2_z).round() as i16,
    ];

    let mut rot: HashMap<u8, (u8, i8)> = HashMap::new();
    for i in 0..3 {
        for j in 0..3 {
            if p1_mod[i].abs() == p2_mod[j].abs() {
                rot.insert(i as u8, (j as u8, (p1_mod[i] / p2_mod[j]) as i8));
            }
        }
    }

    let mut p2_rot: [i16; 3] = [0; 3];

    for i in 0..3 {
        p2_rot[i] =
            p2[rot.get(&(i as u8)).unwrap().0 as usize] * rot.get(&(i as u8)).unwrap().1 as i16;
    }

    let mut trans: [i16; 3] = [0; 3];
    for i in 0..3 {
        trans[i] = p2_rot[i] - p1[i];
    }

    (trans, rot)
}

fn transform_points(trans : &[i16; 3] , rot : &HashMap<u8, (u8, i8)> , points : &Vec<Beacon>) -> HashSet<Beacon>{
    let mut new_points : HashSet<Beacon> = HashSet::new();
    for p in points{
        let mut t = [0;3];
        for i in 0..3{
            t[i] = p[rot[&(i as u8)].0 as usize] * rot[&(i as u8)].1  as i16- trans[i];
        }
        new_points.insert(t);
    }
    new_points
}

fn part_1() -> Vec<[i16;3]>{
    let input = include_str!("input.txt").split("\n\n").collect::<Vec<_>>();

    let mut scanners: Vec<Vec<Beacon>> = Vec::new();
    for s in input {
        let mut s_tmp: Vec<Beacon> = Vec::new();
        for b in s.split("\n").skip(1) {
            let mut t = b.split(",").map(|pos| pos.parse::<i16>().unwrap());
            s_tmp.push([t.next().unwrap(), t.next().unwrap(), t.next().unwrap()]);
        }
        scanners.push(s_tmp);
    }

    let mut grid: HashSet<Beacon> = HashSet::from_iter(scanners[0].iter().cloned());
    scanners.remove(0);

    let mut pos : Vec<[i16;3]> = Vec::new();

    while scanners.len() > 0 {
        let grid_config = get_config(&grid);

        let scanners_common: Vec<_> = scanners
            .iter()
            .map(|s| {
                get_common_pt_num(
                    &grid_config,
                    &get_config(&HashSet::from_iter(s.iter().cloned())),
                )
            })
            .collect();

        let s = scanners_common
            .iter()
            .position(|x| x == scanners_common.iter().max().unwrap())
            .unwrap();

        let (trans, rot) = allign(
            &grid_config,
            &get_config(&HashSet::from_iter(scanners[s].iter().cloned())),
        );

        grid.extend(&transform_points(&trans,&rot,&scanners[s]));
        
        scanners.remove(s);
        pos.push(trans);
    }

    println!("{}" , grid.len());
    pos
}

fn part_2(pos : &Vec<[i16;3]> ) {
    let mut dists :Vec<u16> = Vec::new();
    for p1 in pos{
        for p2 in pos{
            dists.push(distance_taxi(p1,p2));
        }
    }
    println!("{}" , dists.iter().max().unwrap());
}

fn main() {
    let pos = bench(part_1);
    part_2(&pos);
}
