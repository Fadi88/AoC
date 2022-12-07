use std::collections::HashMap;
use std::path::PathBuf;
use std::time;

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}

fn part_1() {
    let mut file_size: HashMap<PathBuf, u32> = HashMap::new();
    let root = PathBuf::from("/");
    let mut pwd = PathBuf::new();

    for l in include_str!("input.txt").split("\n") {
        if l.contains("$") {
            if l.contains(" cd ") {
                if l.contains("/") {
                    pwd = root.clone();
                } else if l.contains("..") {
                    pwd.pop();
                } else {
                    pwd = pwd.join(l.split(" ").last().unwrap());
                }
            }
        } else if !l.contains("dir") {
            let p = l.split(" ").collect::<Vec<_>>();
            file_size.insert(pwd.join(p[1]), p[0].parse::<u32>().unwrap());
        }
    }

    let mut folder_size: HashMap<PathBuf, u32> = HashMap::new();

    for f in file_size {
        for folder in f.0.parent().unwrap().ancestors() {
            *folder_size.entry(folder.to_path_buf()).or_insert(0) += f.1;
        }
    }

    println!(
        "{}",
        folder_size.values().filter(|x| **x <= 100000).sum::<u32>()
    );
}

fn part_2() {
    let mut file_size: HashMap<PathBuf, u32> = HashMap::new();
    let root = PathBuf::from("/");
    let mut pwd = PathBuf::new();

    for l in include_str!("input.txt").split("\n") {
        if l.contains("$") {
            if l.contains(" cd ") {
                if l.contains("/") {
                    pwd = root.clone();
                } else if l.contains("..") {
                    pwd.pop();
                } else {
                    pwd = pwd.join(l.split(" ").last().unwrap());
                }
            }
        } else if !l.contains("dir") {
            let p = l.split(" ").collect::<Vec<_>>();
            file_size.insert(pwd.join(p[1]), p[0].parse::<u32>().unwrap());
        }
    }

    let mut folder_size: HashMap<PathBuf, u32> = HashMap::new();

    for f in file_size {
        for folder in f.0.parent().unwrap().ancestors() {
            *folder_size.entry(folder.to_path_buf()).or_insert(0) += f.1;
        }
    }

    let total_sapce = 70000000;
    let needed_space = 30000000;

    let least_del = needed_space - (total_sapce - folder_size.get(&root).unwrap());

    let mut sorted_size = folder_size.into_iter().map(|x| x.1).collect::<Vec<_>>();

    sorted_size.sort();

    for s in sorted_size {
        if s >= least_del {
            println!("{}", s);
            break;
        }
    }
}

fn main() {
    bench(part_1);
    bench(part_2);
}
