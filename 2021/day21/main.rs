use std::collections::HashMap;
use std::time;

fn bench(f: fn()) {
    let t0 = time::Instant::now();
    let ret = f();
    println!("time used {:?}", time::Instant::now().duration_since(t0));

    ret
}

fn part_1() {
    let mut pos: [u16; 2] = [4, 2];
    let mut score: [u16; 2] = [0; 2];

    let mut dice = 0;

    loop {
        let p1 = 3 * dice + 6;
        let p2 = 3 * dice + 15;
        dice += 3;

        pos[0] = (pos[0] + p1 - 1) % 10 + 1;
        score[0] += pos[0];

        if score[0] >= 1000 {
            break;
        }

        dice += 3;

        pos[1] = (pos[1] + p2 - 1) % 10 + 1;
        score[1] += pos[1];

        if score[1] >= 1000 {
            break;
        }
    }

    println!("{}", *score.iter().min().unwrap() as u32 * dice as u32);
}
fn play_dirac(
    p1: u32,
    p2: u32,
    s1: u32,
    s2: u32,
    player: usize,
    cache: &mut HashMap<(u32, u32, u32, u32, usize), [u64; 2]>,
) -> [u64; 2] {
    if cache.contains_key(&(p1, p2, s1, s2, player)) {
        return *cache.get(&(p1, p2, s1, s2, player)).unwrap();
    }

    let mut wins: [u64; 2] = [0; 2];
    let mut rolls: Vec<_> = Vec::new();
    for r1 in 1..4 {
        for r2 in 1..4 {
            for r3 in 1..4 {
                rolls.push(r1 + r2 + r3);
            }
        }
    }

    for r in rolls {
        let mut pos: [u32; 2] = [p1, p2];
        let mut score: [u32; 2] = [s1, s2];

        pos[player] = (pos[player] + r - 1) % 10 + 1;
        score[player] += pos[player];

        if score[player] >= 21 {
            wins[player] += 1;
        } else {
            let [w1, w2] = play_dirac(
                pos[0],
                pos[1],
                score[0],
                score[1],
                if player == 1 { 0 } else { 1 },
                cache,
            );
            wins[0] += w1;
            wins[1] += w2;
        }
    }
    cache.insert((p1, p2, s1, s2, player), wins);
    cache.insert((p2, p1, s2, s1, if player == 1 { 0 } else { 1 }), [wins[1] , wins[0]]);
    wins
}

fn part_2() {
    let mut cache: HashMap<(u32, u32, u32, u32, usize), [u64; 2]> = HashMap::new();
    println!(
        "{:?}",
        play_dirac(4, 2, 0, 0, 0, &mut cache).iter().max().unwrap()
    );
}

fn main() {
    bench(part_1);
    bench(part_2);
}
