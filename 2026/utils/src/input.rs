use std::fs;
use std::path::Path;
use anyhow::{Context, Result};

pub fn read_input(day: &str) -> Result<String> {
    let path = format!("days/{}/input.txt", day);
    fs::read_to_string(&path)
        .with_context(|| format!("Failed to read input file: {}", path))
}

pub fn read_input_from_file(path: impl AsRef<Path>) -> Result<String> {
    fs::read_to_string(&path)
        .with_context(|| format!("Failed to read input file: {:?}", path.as_ref()))
}
