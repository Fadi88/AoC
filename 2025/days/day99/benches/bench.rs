use criterion::{black_box, criterion_group, criterion_main, Criterion};
use day99::{part_1, part_2};
use utils::read_input;

fn criterion_benchmark(c: &mut Criterion) {
    let input = read_input("day99").expect("Failed to read input");

    c.bench_function("part_1", |b| b.iter(|| part_1(black_box(&input))));
    c.bench_function("part_2", |b| b.iter(|| part_2(black_box(&input))));
}

criterion_group!(benches, criterion_benchmark);
criterion_main!(benches);
