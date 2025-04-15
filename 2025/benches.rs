use criterion::{criterion_group, criterion_main, Criterion};

mod template;

fn template_benchmark(c: &mut Criterion) {
    c.bench_function("template_p1", |b| b.iter(|| template::part_1()));
    c.bench_function("template_p2", |b| b.iter(|| template::part_2()));
}

criterion_group!(benches, template_benchmark);
criterion_main!(benches);
