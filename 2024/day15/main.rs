use std::collections::{HashMap, HashSet};
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

fn free_space(
    robot: (i32, i32),
    d: (i32, i32),
    walls: &HashSet<(i32, i32)>,
    boxes: &HashSet<(i32, i32)>,
) -> (bool, (i32, i32)) {
    let (dx, dy) = d;
    let (mut cx, mut cy) = (robot.0 + dx, robot.1 + dy);

    loop {
        if walls.contains(&(cx, cy)) {
            return (false, (-1, -1));
        }
        if boxes.contains(&(cx, cy)) {
            cx += dx;
            cy += dy;
        } else {
            return (true, (cx, cy));
        }
    }
}

fn part_1() {
    let input = include_str!("input.txt");
    let (g, moves) = input.split_once("\n\n").unwrap();

    let mut robot = (-1, -1);
    let mut boxes = HashSet::new();
    let mut walls = HashSet::new();

    let deltas = [('^', (0, -1)), ('>', (1, 0)), ('v', (0, 1)), ('<', (-1, 0))];

    for (y, l) in g.lines().enumerate() {
        for (x, h) in l.chars().enumerate() {
            match h {
                'O' => {
                    boxes.insert((x as i32, y as i32));
                }
                '#' => {
                    walls.insert((x as i32, y as i32));
                }
                '@' => {
                    robot = (x as i32, y as i32);
                }
                _ => {}
            }
        }
    }

    for m in moves.chars().filter(|c| !c.is_whitespace()) {
        let (dx, dy) = deltas.iter().find(|&&(c, _)| c == m).unwrap().1;
        let (nx, ny) = (robot.0 + dx, robot.1 + dy);

        if !walls.contains(&(nx, ny)) {
            if !boxes.contains(&(nx, ny)) {
                robot = (nx, ny);
            } else {
                let (is_free, next_free) = free_space(robot, (dx, dy), &walls, &boxes);
                if is_free {
                    let mut to_remove = HashSet::new();
                    let mut to_add = HashSet::new();

                    for &b in &boxes {
                        let xs = [robot.0, next_free.0];
                        let ys = [robot.1, next_free.1];
                        if b.0 >= *xs.iter().min().unwrap()
                            && b.0 <= *xs.iter().max().unwrap()
                            && b.1 >= *ys.iter().min().unwrap()
                            && b.1 <= *ys.iter().max().unwrap()
                        {
                            to_remove.insert(b);
                            to_add.insert((b.0 + dx, b.1 + dy));
                        }
                    }
                    boxes = &boxes - &to_remove;
                    boxes = &boxes | &to_add;

                    robot = (robot.0 + dx, robot.1 + dy);
                }
            }
        }
    }

    println!("{}", boxes.iter().map(|&(x, y)| x + 100 * y).sum::<i32>());
}

fn is_free_x(
    robot: (i32, i32),
    dx: i32,
    walls: &HashSet<(i32, i32)>,
    boxes: &HashSet<((i32, i32), (i32, i32))>,
) -> (bool, i32) {
    let wx: HashSet<i32> = walls
        .iter()
        .filter(|w| w.1 == robot.1)
        .map(|w| w.0)
        .collect();
    let bx: HashSet<i32> = boxes
        .iter()
        .filter(|&&(b1, _)| b1.1 == robot.1)
        .map(|&(b1, _)| b1.0)
        .collect();

    let mut cx = robot.0 + dx;
    loop {
        if wx.contains(&cx) {
            return (false, -1);
        }
        if bx.contains(&cx) {
            cx += dx;
        } else {
            return (true, cx);
        }
    }
}

fn is_free_y(
    robot: (i32, i32),
    dy: i32,
    walls: &HashSet<(i32, i32)>,
    boxes: &HashSet<((i32, i32), (i32, i32))>,
) -> (bool, Option<HashSet<((i32, i32), (i32, i32))>>) {
    let mut to_move: HashSet<((i32, i32), (i32, i32))> = boxes
        .iter()
        .filter(|&&(b1, b2)| robot.0 == b1.0 || robot.0 == b2.0 && robot.1 + dy == b1.1)
        .cloned()
        .collect();

    let mut top: Vec<((i32, i32), (i32, i32))> = to_move.iter().cloned().collect();

    loop {
        let mut new_top = Vec::new();
        let mut added = false;

        for (b1, b2) in top {
            let mut xs = HashMap::new();
            for &(nb1, nb2) in boxes {
                for &x in &[nb1.0, nb2.0] {
                    if nb1.1 == b1.1 + dy {
                        xs.insert(x, (nb1, nb2));
                    }
                }
            }

            let to_add: HashSet<((i32, i32), (i32, i32))> = [b1.0, b2.0]
                .iter()
                .filter_map(|&x| xs.get(&x).cloned())
                .collect();

            if !to_add.is_empty() {
                new_top.extend(to_add.iter().cloned());
                to_move.extend(to_add);
                added = true;
            } else {
                new_top.push((b1, b2));
            }
        }

        top = new_top;

        if !added {
            break;
        }
    }

    for &(b1, b2) in &to_move {
        if walls.contains(&(b1.0, b1.1 + dy)) || walls.contains(&(b2.0, b2.1 + dy)) {
            return (false, None);
        }
    }

    (true, Some(to_move))
}

fn part_2() {
    let input_file = include_str!("input.txt");
    let (g, moves) = input_file.split_once("\n\n").unwrap();

    let mut robot = (-1, -1);
    let mut boxes = HashSet::new();
    let mut walls = HashSet::new();

    let deltas = [('^', (0, -1)), ('>', (1, 0)), ('v', (0, 1)), ('<', (-1, 0))];

    for (y, l) in g.lines().enumerate() {
        for (x, h) in l.chars().enumerate() {
            match h {
                'O' => {
                    boxes.insert(((2 * x as i32, y as i32), (2 * x as i32 + 1, y as i32)));
                }
                '#' => {
                    walls.insert((2 * x as i32, y as i32));
                    walls.insert((2 * x as i32 + 1, y as i32));
                }
                '@' => {
                    robot = (2 * x as i32, y as i32);
                }
                _ => {}
            }
        }
    }

    for m in moves.chars().filter(|c| !c.is_whitespace()) {
        let (dx, dy) = deltas.iter().find(|&&(c, _)| c == m).unwrap().1;

        if walls.contains(&(robot.0 + dx, robot.1 + dy)) {
            continue;
        }

        if dy == 0 {
            let (is_free, next_free) = is_free_x(robot, dx, &walls, &boxes);
            if is_free {
                let min_x = std::cmp::min(next_free, robot.0);
                let max_x = std::cmp::max(next_free, robot.0);
                let to_move: HashSet<((i32, i32), (i32, i32))> = boxes
                    .iter()
                    .filter(|&&(b1, _)| b1.1 == robot.1 && b1.0 >= min_x && b1.0 <= max_x)
                    .cloned()
                    .collect();

                boxes = &boxes - &to_move;
                let new_boxes: HashSet<((i32, i32), (i32, i32))> = to_move
                    .iter()
                    .map(|&(b1, b2)| ((b1.0 + dx, b1.1), (b2.0 + dx, b2.1)))
                    .collect();
                boxes = &boxes | &new_boxes;

                robot = (robot.0 + dx, robot.1);
            }
        } else {
            let up: HashSet<((i32, i32), (i32, i32))> = boxes
                .iter()
                .filter(|&&(b1, b2)| (robot.0 == b1.0 || robot.0 == b2.0) && robot.1 + dy == b1.1)
                .cloned()
                .collect();

            if up.is_empty() {
                robot = (robot.0, robot.1 + dy);
            } else {
                let (is_free, to_move) = is_free_y(robot, dy, &walls, &boxes);

                if is_free {
                    if let Some(to_move) = to_move {
                        boxes = &boxes - &to_move;
                        let new_boxes: HashSet<((i32, i32), (i32, i32))> = to_move
                            .iter()
                            .map(|&(b1, b2)| ((b1.0, b1.1 + dy), (b2.0, b2.1 + dy)))
                            .collect();
                        boxes = &boxes | &new_boxes;
                    }

                    robot = (robot.0, robot.1 + dy);
                }
            }
        }
    }

    println!(
        "{}",
        boxes.iter().map(|&(b, _)| b.0 + 100 * b.1).sum::<i32>()
    );
}

fn main() {
    bench(part_1);
    bench(part_2);
}
