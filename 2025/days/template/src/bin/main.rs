use anyhow::Result;
use day_template::{part_1, part_2};
use utils::{read_input, run_part};

fn main() -> Result<()> {
    // Read input for the current day (this will need to be updated by the script)
    // For the template, we can just use a placeholder or expect "template"
    let input = read_input("template")?;

    run_part("Part 1", || part_1(&input).unwrap());
    run_part("Part 2", || part_2(&input).unwrap());

    Ok(())
}
