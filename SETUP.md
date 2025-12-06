# 🛠️ Setup & Usage Guide

This repository contains Advent of Code solutions in **Python**, **Rust**, and occasionally **C++**. Below you will find instructions on how to set up your environment and run the solutions.

## 🐍 Python

### Prerequisites
*   **Python 3.10+**: [Download Here](https://www.python.org/downloads/)
*   **PyPy** (Optional, for speed): [Download Here](https://www.pypy.org/download.html)

### Running a Solution
Navigate to the specific day's directory and run:

```bash
# Standard Python
python solution.py

# Using PyPy
pypy solution.py
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

# Benchmarking
cargo bench -p day01
```

### Legacy Rust (Pre-2025)
For older years (e.g., 2022), navigate to the year folder and run:
```bash
cd 2022
cargo run --release --bin day01
```

---

## ⚡ C++

Used mainly in 2018.

### Building
1.  Navigate to the year folder:
    ```bash
    cd 2018
    ```
2.  Generate build files:
    ```bash
    mkdir build && cd build && cmake ..
    ```
3.  Compile:
    ```bash
    make day01 && cmake --install day01
    ```
4.  Run:
    ```bash
    cd install/day01 && ./day01
    ```

---

## 📥 Fetching Inputs automatically

This template uses `advent-of-code-data` to automatically fetch your puzzle inputs.

1.  **Install the tool:**
    ```bash
    pip install advent-of-code-data
    ```

2.  **Authentication:**
    *   Log in to Advent of Code in your browser.
    *   Find your `session` cookie (F12 -> Application -> Cookies).
    *   Create a `.env` file in the `2025` directory (or root).
    *   Add: `AOC_SESSION=your_copied_cookie_value`

3.  **Usage:**
    When you run `python3 new_day.py`, it will automatically download `input.txt`.
