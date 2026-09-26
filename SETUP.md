# 🛠️ Setup & Usage Guide

This repository contains Advent of Code solutions in **Python**, **Rust**, and occasionally **C++**. Below you will find instructions on how to set up your environment and run the solutions.

## 🐍 Python

### Prerequisites
*   **Python 3.10+**: [Download Here](https://www.python.org/downloads/)
*   **PyPy** (Optional, for speed): [Download Here](https://www.pypy.org/download.html)
*   **Dependencies** (numpy, scipy, shapely, networkx, ...):
    ```bash
    pip install -r requirements.txt
    ```

### Running a Solution
Navigate to the specific day's directory and run the solution file. From 2025 onwards it is `days/dayXX/solution.py`; earlier years use `dayXX/code.py`.

```bash
# Standard Python
python solution.py   # or: python code.py

# Using PyPy
pypy solution.py
```

### Checking the Repository
`check.py` verifies that every year has a solution for each day and that each Python solution defines its `part1`/`part_1` and `part2`/`part_2` functions:

```bash
python check.py
```

---

## 🦀 Rust (2025+)

Starting from 2025, the project uses a Cargo Workspace structure.

### Prerequisites
*   **Rust Toolchain**: [Install Here](https://www.rust-lang.org/tools/install)

### Setup
1.  Navigate to the 2025 directory:
    ```bash
    cd 2025
    ```
2.  Create a new day (bootstraps files):
    ```bash
    python3 new_day.py <day_number>
    # Example: python3 new_day.py 5
    ```

### Running Solutions
You can run solutions directly from the `2025` root using the package name (`dayXX`).

```bash
# Debug Mode (slower, better error checks)
cargo run -p day01

# Release Mode (fast!)
cargo run --release -p day01

# Tests (needs days/day01/input.txt)
cargo test -p day01

# Benchmarking
cargo bench -p day01
```

### Updating the Benchmark Table
Every number in the README table comes from `update_benchmarks.py`; don't edit them by hand. For each day it runs the Python solution 5 times and takes the median of each part, and runs `cargo bench --bench bench` for the Rust version (Criterion's estimate). Missing inputs are downloaded first.

```bash
python update_benchmarks.py --all  # re-run every day (what the README shows)
python update_benchmarks.py        # new days only
python update_benchmarks.py 1 2 3  # re-run days 1-3
```

Below the table the script writes the date, CPU, OS, Python and rustc versions it measured with, plus the command it was run with. Timings depend on the machine, so compare numbers from the same setup.

### Legacy Rust (2021-2024)
Each of these years is a single Cargo package with one binary per day. The inputs are embedded at compile time, so `dayXX/input.txt` must exist before building. Navigate to the year folder and run:
```bash
cd 2022
cargo run --release --bin day01
```

---

## ⚡ C++

Used for 2019 (except day 20, which is Python) and days 1-2 of 2018. Each year is its own CMake project, because both define targets named `day01`, `day02`, and so on. The root `CMakeLists.txt` builds 2019 only.

### Building 2019
1.  Navigate to the year folder:
    ```bash
    cd 2019
    ```
2.  Generate build files:
    ```bash
    mkdir build && cd build && cmake ..
    ```
3.  Compile and install one day (this copies `day01/input.txt` next to the binary):
    ```bash
    cmake --build . --target day01 && cmake --install day01
    ```
4.  Run:
    ```bash
    cd install/day01 && ./day01
    ```

### Building 2018
```bash
cd 2018
mkdir build && cd build && cmake ..
cmake --build . --target day01
```

---

## 📥 Fetching Inputs automatically

The 2025 tooling uses `advent-of-code-data` to automatically fetch your puzzle inputs.

Advent of Code asks that puzzle inputs aren't shared, so they must never be committed. `.gitignore` covers `input.txt`, `.env` and output generated from inputs, and a pre-commit hook refuses them even if they're force-added. Enable it once per clone:

```bash
git config core.hooksPath .githooks
```

CI runs the same check against every tracked file.

1.  **Install the tool** (also included in `requirements.txt`):
    ```bash
    pip install advent-of-code-data
    ```

2.  **Authentication:**
    *   Log in to Advent of Code in your browser.
    *   Find your `session` cookie (F12 -> Application -> Cookies).
    *   Create a `.env` file in the `2025` directory containing `AOC_SESSION=your_copied_cookie_value`, or set `AOC_SESSION` as an environment variable.

3.  **Usage:**
    `python3 new_day.py <day>` downloads `input.txt` for the new day, and `update_benchmarks.py` downloads any input that is missing.

---

## 🐳 Dev Container

`.devcontainer/` defines a Debian-based container with Rust (plus clippy), Python 3, CMake and g++. When the container is created it runs `pip install -r requirements.txt`. Open the repository in VS Code and choose **Reopen in Container**.
