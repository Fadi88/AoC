use criterion::{black_box, criterion_group, criterion_main, Criterion};
use day_template::{part_1, part_2};
use utils::read_input;

fn criterion_benchmark(c: &mut Criterion) {
    let input_path = concat!(env!("CARGO_MANIFEST_DIR"), "/input.txt");
    let input = utils::read_input_from_file(input_path).expect("Failed to read input");

    c.bench_function("part_1", |b| b.iter(|| part_1(black_box(&input))));
    c.bench_function("part_2", |b| b.iter(|| part_2(black_box(&input))));
}

criterion_group!(benches, criterion_benchmark);
criterion_main!(benches);
