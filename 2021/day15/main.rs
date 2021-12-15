use std::collections::VecDeque;
use std::time;

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}

fn part_1() {
    let mut grid: Vec<Vec<u8>> = Vec::new();
    for l in include_str!("test.txt").split('\n') {
        grid.push(
            l.chars()
                .map(|x| x.to_digit(10).unwrap() as u8)
                .collect::<Vec<u8>>(),
        );
    }

    let deltas : [(i16,i16);4]= [(0, 1), (0, -1), (1, 0), (-1, 0)];

    let mut to_visit: VecDeque<Vec<(i16, i16)>> = VecDeque::new();
    to_visit.push_back(vec![(0, 0)]);

    let mut score: Vec<u32> = Vec::new();
    while !to_visit.is_empty() {
        let path = to_visit.pop_front().unwrap();
        let (x, y) = path.last().unwrap();
        if *x == grid.len() as i16 && *y == grid.last().unwrap().len() as i16 {
            let tmp = path
                .iter()
                .skip(1)
                .map(|p| grid[p.0 as usize][p.1 as usize] as u32)
                .collect::<Vec<u32>>()
                .iter()
                .sum::<u32>();
            score.push(tmp);
            continue;
        }
 
        for (dx, dy) in deltas {
            if *x + dx >= 0
                && x + dx < grid.len() as i16
                && y + dy >= 0
                && y + dy < grid[0].len() as i16
            {
                let mut tmp = path.clone();
                tmp.push((x+dx,y+dy));
                to_visit.push_back(tmp); 
            }
        }
    }

    println!("{}" , score.iter().min().unwrap());
}

fn part_2() {}

fn main() {
    bench(part_1);
    bench(part_2);
}
