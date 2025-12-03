use anyhow::Result;
use day03::{part_1, part_2};
use utils::run_part;

fn main() -> Result<()> {
    // Read input for the current day (automatically found relative to the crate)
    run_part("Part 1", || part_1().unwrap());
    run_part("Part 2", || part_2().unwrap());

    Ok(())
}
