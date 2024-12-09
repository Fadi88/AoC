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

fn part_1() {
    let disk = include_str!("input.txt").trim();

    let mut layout: Vec<_> = disk
        .chars()
        .enumerate()
        .flat_map(|(idx, ch)| {
            let c = if idx % 2 == 0 {
                (idx / 2).to_string()
            } else {
                ".".to_string()
            };
            std::iter::repeat(c).take(ch.to_digit(10).unwrap() as usize)
        })
        .collect();

    while layout.contains(&".".to_string()) {
        let pos = layout.iter().position(|x| x == &".".to_string()).unwrap();
        let n = layout.pop().unwrap();
        layout[pos] = n;

        while layout.last() == Some(&".".to_string()) {
            layout.pop();
        }
    }

    let checksum: u64 = layout
        .iter()
        .enumerate()
        .map(|(i, c)| c.parse::<u64>().unwrap() * i as u64) // Parse to i32
        .sum();

    println!("{}", checksum);
}

fn clean_free(free_space: &mut Vec<(u64, u64)>) -> Vec<(u64, u64)> {
    let mut new_free_space = Vec::new();
    free_space.sort_by_key(|x| x.0); // Sort by starting position

    for &(fpos, fsize) in free_space.iter() {
        if fsize == 0 {
            continue;
        }

        if new_free_space.is_empty() {
            new_free_space.push((fpos, fsize));
        } else {
            if new_free_space.last().unwrap().0 + new_free_space.last().unwrap().1 == fpos {
                // Merge with the previous interval
                let last = new_free_space.pop().unwrap();
                new_free_space.push((last.0, last.1 + fsize));
            } else {
                new_free_space.push((fpos, fsize));
            }
        }
    }

    new_free_space
}

fn part_2() {
    let input = include_str!("input.txt");

    let mut pos = 0;

    let mut files = Vec::new(); // (id, pos, size)
    let mut free_space = Vec::new(); // (pos, size)

    for (idx, ch) in input.chars().enumerate() {
        let size = ch.to_digit(10).unwrap() ; // Use i64 to prevent potential overflow

        if idx % 2 == 0 {
            files.push((idx as u64 /2 as u64, pos as u64, size as u64));
        } else {
            free_space.push((pos as u64, size as u64));
        }

        pos += size;
    }

    for fidx in (0..files.len()).rev() {
        let (fid, fpos, fsize) = files[fidx];
        if fsize == 0 {
            continue;
        }

        for i in 0..free_space.len() {
            let (free_pos, free_size) = free_space[i];

            if fsize <= free_size && free_pos < fpos {
                files[fidx] = (fid, free_pos, fsize);

                if free_size == fsize {
                    free_space.remove(i);
                } else {
                    free_space[i] = (free_pos + fsize, free_size - fsize);
                }

                free_space.push((fpos, fsize));

                free_space = clean_free(& mut free_space);

                break;
            }
        }
    }

    
    let checksum: u64 = files
        .iter()
        .flat_map(|(fid, fpos, fsize)| {
            (0..*fsize).map(move |i|(*fpos + i as u64) * (*fid as u64) as u64)
        })
        .sum();

    println!("{}", checksum);
}

fn main() {
    bench(part_1);
    bench(part_2);
}
