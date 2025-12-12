use anyhow::Result;
use day12::part_1;
use std::time::Instant;

fn main() -> Result<()> {
    let start = Instant::now();
    let result = part_1()?;
    println!("Part 1 Result: {}", result);
    println!("Time: {:?}", start.elapsed());
    Ok(())
}
