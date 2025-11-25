# adventofcode

solutions for [advent of code](https://adventofcode.com)

language used : C++ and python and sometimes also Rust

## How to run the code

each year has a folder and each day has a folder, input is usually stored as input.txt in the same folder and testing input is stored as test.txt if it was used.

if you want to test the code with a different input just replace the content of the file.

sometimes however if the input is a as simple a single number it is stored in the code itself as a variable and not as a file.

### Python

It is recommend to install python ver 3 instructions can be found [here](https://www.python.org/downloads/)

for faster execution maybe use pypy from [here](https://www.pypy.org/download.html)

to run just CD to directory of each day and try
```
python code.py
```

or 

```
pypy code.py
```

### RUST

install rust as documented [here](https://www.rust-lang.org/tools/install)

navigate to the year folder for example 2022

## Fetching Inputs

This template uses `advent-of-code-data` to automatically fetch your puzzle inputs.

1.  **Install the tool:**
    ```bash
    pip install advent-of-code-data
    ```
    (This is already included in the Dev Container).

2.  **Authentication:**
    The tool needs your Advent of Code session cookie to download inputs.
    
    1.  **Get your cookie:**
        - Log in to Advent of Code in your browser.
        - Open Developer Tools (F12) -> Application/Storage -> Cookies.
        - Copy the value of the `session` cookie.
    2.  **Set it in `.env`:**
        - Create or open the `.env` file in the root directory.
        - Paste your cookie: `AOC_SESSION=your_copied_cookie_value`

3.  **Usage:**
    When you create a new day using `python3 2025/new_day.py <day>`, the input will be automatically downloaded to `2025/day<day>/input.txt`.


```
cd AoC\2022
```

to run the code in debug mode.

```
cargo run --bin day{XY} # XY can be from 01 to 25
```

to run the code in debug mode.

```
cargo run --release --bin day{XY} # XY can be from 01 to 25
```

debug mode is useful for error detection, sometimes code just works in release mode
but in debug mode it is able to detect big issues (like overflow,underflow etc...)

### Rust (2025+)

Starting from 2025, the project uses a Cargo Workspace structure.

**Setup:**
1. Navigate to the 2025 directory: `cd 2025`
2. Create a new day: `python3 new_day.py <day_number>` (e.g., `python3 new_day.py 1`)

**Running (Rust):**
- Run a specific day: `cargo run -p day<day_number>` (e.g., `cargo run -p day01`)
- Run with release profile: `cargo run --release -p day<day_number>`

**Running (Python):**
- Navigate to the day's directory: `cd days/day<day_number>`
- Run the solution: `python3 solution.py`

**Benchmarking (Rust):**
- Run benchmarks for a day: `cargo bench -p day<day_number>`

### C++

only 2018 mainly and some days here in there

first we need to create make based on the cmake
```
cd 2018
mkdir build && cd build && cmake ..
```

to build day{XX} (where XX is from 00 to 25)
```
make day{XX} && cmake --install day{XX}
```

to run day{XX}
```
cd install/day{XX} && ./day{XX}
```

### TODO

- create a devcontainer with docker that includes all the tools.

- add cmake section to the docu
- make cmake more consistent 

