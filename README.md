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

