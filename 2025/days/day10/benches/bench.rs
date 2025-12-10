use criterion::{criterion_group, criterion_main, Criterion};
use day10::{part_1, part_2};

fn criterion_benchmark(c: &mut Criterion) {
    let input = std::fs::read_to_string("input.txt").unwrap();
    let machines = day10::parse(&input);

    c.bench_function("solve_part_2_no_io", |b| {
        b.iter(|| day10::solve_all(&machines))
    });
}

criterion_group!(benches, criterion_benchmark);
criterion_main!(benches);
