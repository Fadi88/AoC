use criterion::{criterion_group, criterion_main, Criterion};
use day12::{part_1, part_2};

fn criterion_benchmark(c: &mut Criterion) {
    c.bench_function("part_1", |b| b.iter(|| part_1()));
    c.bench_function("part_2", |b| b.iter(|| part_2()));
}

criterion_group!(benches, criterion_benchmark);
criterion_main!(benches);
