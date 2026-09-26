cmake_minimum_required (VERSION 3.8)

project(AoC)

# 2018 is a separate CMake project: its targets (day01, day02) clash with 2019's.
# Build it from the 2018 folder instead (see SETUP.md).
add_subdirectory(2019)
