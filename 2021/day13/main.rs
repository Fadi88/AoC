use std::collections::HashSet;
use std::time;

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}

fn part_1() {
    let mut dots: HashSet<(u16, u16)> = HashSet::new();

    'lines: for l in include_str!("input.txt").split('\n') {
        let mut new_dots: HashSet<(u16, u16)> = HashSet::new();

        if l.contains(',') {
            let mut p = l.split(',').map(|x| x.parse::<u16>().unwrap());
            dots.insert((p.next().unwrap(), p.next().unwrap()));
        } else if l.contains("fold") {
            let mut fold = l.split('=');

            let axe = fold.next().unwrap();
            let loc = fold.next().unwrap().parse::<u16>().unwrap();

            if axe.contains('x') {
                for (x, y) in &dots {
                    if x > &loc {
                        new_dots.insert((loc - (x - loc), *y));
                    } else {
                        new_dots.insert((*x, *y));
                    }
                }
            } else {
                for (x, y) in &dots {
                    if y > &loc {
                        new_dots.insert((*x, (loc - (y - loc))));
                    } else {
                        new_dots.insert((*x, *y));
                    }
                }
            }

            println!("{:?}", new_dots.len());
            break 'lines;
        }
    }
}

fn part_2() {
    let mut dots: HashSet<(u16, u16)> = HashSet::new();

    for l in include_str!("input.txt").split('\n') {
        let mut new_dots: HashSet<(u16, u16)> = HashSet::new();

        if l.contains(',') {
            let mut p = l.split(',').map(|x| x.parse::<u16>().unwrap());
            dots.insert((p.next().unwrap(), p.next().unwrap()));
        } else if l.contains("fold") {
            let mut fold = l.split('=');

            let axe = fold.next().unwrap();
            let loc = fold.next().unwrap().parse::<u16>().unwrap();

            if axe.contains('x') {
                for (x, y) in &dots {
                    if x > &loc {
                        new_dots.insert((loc - (x - loc), *y));
                    } else {
                        new_dots.insert((*x, *y));
                    }
                }
            } else {
                for (x, y) in &dots {
                    if y > &loc {
                        new_dots.insert((*x, (loc - (y - loc))));
                    } else {
                        new_dots.insert((*x, *y));
                    }
                }
            }

            dots = new_dots;
        }
    }

    let max_x = dots.iter().max_by(|p1, p2| p1.0.cmp(&p2.0)).unwrap().0;
    let max_y = dots.iter().max_by(|p1, p2| p1.1.cmp(&p2.1)).unwrap().1;

    for y in 0..=max_y{
        for x in 0..=max_x{
            if dots.contains(&(x,y)){
                print!("x");
            } else {
                print!(" "); 
            }
        }
        println!("");
    }
}

fn main() {
    bench(part_1);
    bench(part_2);
}
