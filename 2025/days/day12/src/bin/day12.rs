use anyhow::Result;
use day12::part_1;
use utils::run_part;

fn main() -> Result<()> {
    // Read input for the current day (automatically found relative to the crate)
    let input_path = concat!(env!("CARGO_MANIFEST_DIR"), "/input.txt");
    let input = utils::read_input_from_file(input_path)?;

    run_part("Part 1", || part_1(&input).unwrap());

    Ok(())
}
