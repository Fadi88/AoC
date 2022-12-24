use std::collections::HashMap;
use std::collections::HashSet;
use std::collections::VecDeque;
use std::fs;
use std::time;

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}
#[derive(Eq, Hash, PartialEq, Clone)]
struct Blizzard {
    direction: char,
    pos: (u8, u8),
}

fn cycle_grid(grid: &HashSet<Blizzard>, max_x: u8, max_y: u8) -> HashSet<Blizzard> {
    let mut new_grid: HashSet<Blizzard> = HashSet::new();

    for b in grid {
        let (mut x, mut y) = b.pos;

        match b.direction {
            '>' => {
                x += 1;
                if x == max_x {
                    x = 1;
                }
            }
            '<' => {
                x -= 1;
                if x == 0 {
                    x = max_x - 1;
                }
            }
            'v' => {
                y += 1;
                if y == max_y {
                    y = 1;
                }
            }
            '^' => {
                y -= 1;
                if y == 0 {
                    y = max_y - 1;
                }
            }
            _ => unreachable!(),
        }

        new_grid.insert(Blizzard {
            direction: b.direction,
            pos: (x, y),
        });
    }

    new_grid
}

fn part_1() {
    let mut grid: HashSet<Blizzard> = HashSet::new();
    let mut max_x: u8 = 0;
    let mut max_y: u8 = 0;

    for (y, l) in fs::read_to_string("input.txt").unwrap().lines().enumerate() {
        for (x, c) in l.chars().enumerate() {
            if ['<', '>', '^', 'v'].contains(&c) {
                grid.insert(Blizzard {
                    direction: c,
                    pos: (x as u8, y as u8),
                });
            }
            max_x = max_x.max(x as u8);
        }
        max_y = max_y.max(y as u8);
    }

    let target = ((max_x - 1) as u8, (max_y) as u8);
    let start = (1 as u8, 0 as u8);

    let mut history: HashMap<u16, HashSet<Blizzard>> = HashMap::new();
    history.insert(0, grid.clone());

    let mut occupied: HashMap<u16, HashSet<(u8, u8)>> = HashMap::new();
    occupied.insert(0, grid.iter().map(|x| x.pos).collect());

    let deltas: [(i8, i8); 4] = [(0, 1), (1, 0), (0, -1), (-1, 0)];

    let mut to_visit: VecDeque<((u8, u8), u16)> = VecDeque::new();
    to_visit.push_back((start, 0));

    let mut seen: HashSet<((u8, u8), u16)> = HashSet::new();

    while !to_visit.is_empty() {
        let (current_pos, current_step) = to_visit.pop_front().unwrap();

        if seen.contains(&(current_pos, current_step)) {
            continue;
        }

        seen.insert((current_pos, current_step));

        if !history.contains_key(&(current_step + 1)) {
            let n_grid = cycle_grid(&history.get(&current_step).unwrap(), max_x, max_y);
            occupied.insert(current_step + 1, n_grid.iter().map(|x| x.pos).collect());
            history.insert(current_step + 1, n_grid);
        }

        // option 1 to wait for 1 minute
        if !occupied
            .get(&(current_step + 1))
            .unwrap()
            .contains(&current_pos)
        {
            to_visit.push_back((current_pos, current_step + 1));
        }

        for (dx, dy) in deltas {
            let (nx, ny) = (
                (current_pos.0 as i8 + dx) as u8,
                (current_pos.1 as i8 + dy) as u8,
            );

            if (nx, ny) == target {
                println!("{}", current_step + 1);
                return;
            }
            if nx > 0 && nx < max_x && ny > 0 && ny < max_y {
                if !occupied
                    .get(&(current_step + 1))
                    .unwrap()
                    .contains(&(nx, ny))
                {
                    to_visit.push_back(((nx, ny), current_step + 1));
                }
            }
        }
    }
}

fn part_2() {
    let mut grid: HashSet<Blizzard> = HashSet::new();
    let mut max_x: u8 = 0;
    let mut max_y: u8 = 0;

    for (y, l) in fs::read_to_string("input.txt").unwrap().lines().enumerate() {
        for (x, c) in l.chars().enumerate() {
            if ['<', '>', '^', 'v'].contains(&c) {
                grid.insert(Blizzard {
                    direction: c,
                    pos: (x as u8, y as u8),
                });
            }
            max_x = max_x.max(x as u8);
        }
        max_y = max_y.max(y as u8);
    }

    let target = ((max_x - 1) as u8, (max_y) as u8);
    let start = (1 as u8, 0 as u8);

    let mut history: HashMap<u16, HashSet<Blizzard>> = HashMap::new();
    history.insert(0, grid.clone());

    let mut occupied: HashMap<u16, HashSet<(u8, u8)>> = HashMap::new();
    occupied.insert(0, grid.iter().map(|x| x.pos).collect());

    let deltas: [(i8, i8); 4] = [(0, 1), (1, 0), (0, -1), (-1, 0)];

    let mut to_visit: VecDeque<((u8, u8), u16)> = VecDeque::new();
    to_visit.push_back((start, 0));

    let mut seen: HashSet<((u8, u8), u16)> = HashSet::new();

    let mut times: Vec<u16> = Vec::new();

    while !to_visit.is_empty() {
        let (current_pos, current_step) = to_visit.pop_front().unwrap();

        if seen.contains(&(current_pos, current_step)) {
            continue;
        }

        seen.insert((current_pos, current_step));

        if !history.contains_key(&(current_step + 1)) {
            let n_grid = cycle_grid(&history.get(&current_step).unwrap(), max_x, max_y);
            occupied.insert(current_step + 1, n_grid.iter().map(|x| x.pos).collect());
            history.insert(current_step + 1, n_grid);
        }

        // option 1 to wait for 1 minute
        if !occupied
            .get(&(current_step + 1))
            .unwrap()
            .contains(&current_pos)
        {
            to_visit.push_back((current_pos, current_step + 1));
        }

        for (dx, dy) in deltas {
            let (nx, ny) = (
                (current_pos.0 as i8 + dx) as u8,
                (current_pos.1 as i8 + dy) as u8,
            );

            if (nx, ny) == target {
                if times.len() == 0 {
                    times.push(current_step + 1);
                    to_visit.clear();
                    to_visit.push_back((target, current_step + 1));
                    break;
                }
                if times.len() == 2 {
                    println!("{}", current_step + 1);
                    return;
                }
            }
            if (nx, ny) == start {
                if times.len() == 1 {
                    times.push(current_step + 1);
                    to_visit.clear();
                    to_visit.push_back((start, current_step + 1));
                    break;
                }
            }
            if nx > 0 && nx < max_x && ny > 0 && ny < max_y {
                if !occupied
                    .get(&(current_step + 1))
                    .unwrap()
                    .contains(&(nx, ny))
                {
                    to_visit.push_back(((nx, ny), current_step + 1));
                }
            }
        }
    }
}

fn main() {
    bench(part_1);
    bench(part_2);
}
