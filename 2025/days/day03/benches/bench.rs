use criterion::{criterion_group, criterion_main, Criterion};
use day03::{part_1, part_2};

fn criterion_benchmark(c: &mut Criterion) {
    let input = std::fs::read_to_string("input.txt").unwrap();
    c.bench_function("part_1", |b| b.iter(|| part_1(&input)));
    c.bench_function("part_2", |b| b.iter(|| part_2(&input)));
}

criterion_group!(benches, criterion_benchmark);
criterion_main!(benches);
