use std::cmp::Ordering;
use std::collections::BinaryHeap;
use std::collections::HashMap;
use std::time;

#[derive(Copy, Clone, Eq, PartialEq)]
struct Point {
    cost: u16,
    pos: (u16, u16),
}

impl Ord for Point {
    fn cmp(&self, other: &Self) -> Ordering {
        other
            .cost
            .cmp(&self.cost)
            .then_with(|| self.pos.cmp(&other.pos))
    }
}

impl PartialOrd for Point {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}

fn part_1() {
    let mut grid: Vec<Vec<u8>> = Vec::new();
    for l in include_str!("input.txt").split('\n') {
        grid.push(
            l.chars()
                .map(|x| x.to_digit(10).unwrap() as u8)
                .collect::<Vec<u8>>(),
        );
    }

    let deltas: [(i16, i16); 4] = [(0, 1), (0, -1), (1, 0), (-1, 0)];

    let mut visit: BinaryHeap<Point> = BinaryHeap::new();

    visit.push(Point {
        cost: 0,
        pos: (0, 0),
    });

    let mut risk: HashMap<(i16, i16), u16> = HashMap::new();
    risk.insert((0, 0), 0);

    while let Some(Point { cost, pos }) = visit.pop() {
        for (dx, dy) in deltas {
            if pos.0 as i16 + dx >= 0
                && pos.0 as i16 + dx < grid.len() as i16
                && pos.1 as i16 + dy >= 0
                && pos.1 as i16 + dy < grid[0].len() as i16
            {
                let new_risk =
                    cost + grid[(pos.0 as i16 + dx) as usize][(pos.1 as i16 + dy) as usize] as u16;
                if *risk
                    .entry(((pos.0 as i16 + dx), (pos.1 as i16 + dy)))
                    .or_insert(u16::MAX)
                    > new_risk
                {
                    risk.insert(((pos.0 as i16 + dx), (pos.1 as i16 + dy)), new_risk);
                    visit.push(Point {
                        cost: new_risk,
                        pos: ((pos.0 as i16 + dx) as u16, (pos.1 as i16 + dy) as u16),
                    });
                }
            }
        }
    }

    println!(
        "{}",
        risk.get(&((grid.len() - 1) as i16, (grid[0].len() - 1) as i16))
            .unwrap()
    );
}

fn get_risk(grid: &Vec<Vec<u8>>, x: u16, y: u16) -> u8 {
    let tmp = grid[x as usize % grid.len()][y as usize % grid[0].len()] as u16
        + (x / grid.len() as u16)
        + (y / grid[0].len() as u16);
    (tmp as u8 - 1) % 9 + 1
}

fn part_2() {
    let mut grid: Vec<Vec<u8>> = Vec::new();
    for l in include_str!("input.txt").split('\n') {
        grid.push(
            l.chars()
                .map(|x| x.to_digit(10).unwrap() as u8)
                .collect::<Vec<u8>>(),
        );
    }

    let deltas: [(i16, i16); 4] = [(0, 1), (0, -1), (1, 0), (-1, 0)];

    let mut visit: BinaryHeap<Point> = BinaryHeap::new();

    visit.push(Point {
        cost: 0,
        pos: (0, 0),
    });

    let mut risk: HashMap<(i16, i16), u16> = HashMap::new();
    risk.insert((0, 0), 0);

    while let Some(Point { cost, pos }) = visit.pop() {
        for (dx, dy) in deltas {
            if pos.0 as i16 + dx >= 0
                && pos.0 as i16 + dx < 5 * grid.len() as i16
                && pos.1 as i16 + dy >= 0
                && pos.1 as i16 + dy < 5 * grid[0].len() as i16
            {
                let new_risk = cost
                    + get_risk(
                        &grid,
                        (pos.0 as i16 + dx) as u16,
                        (pos.1 as i16 + dy) as u16,
                    ) as u16;
                if *risk
                    .entry(((pos.0 as i16 + dx), (pos.1 as i16 + dy)))
                    .or_insert(u16::MAX)
                    > new_risk
                {
                    risk.insert(((pos.0 as i16 + dx), (pos.1 as i16 + dy)), new_risk);
                    visit.push(Point {
                        cost: new_risk,
                        pos: ((pos.0 as i16 + dx) as u16, (pos.1 as i16 + dy) as u16),
                    });
                }
            }
        }
    }

    println!(
        "{}",
        risk.get(&((5 * grid.len() - 1) as i16, (5 * grid[0].len() - 1) as i16))
            .unwrap()
    );
}

fn main() {
    bench(part_1);
    bench(part_2);
}
