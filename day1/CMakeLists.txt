cmake_minimum_required(VERSION 3.0)

add_executable(day1_1 day1-1.cpp)
add_executable(day1_2 day1-2.cpp)

install(TARGETS day1_1 day1_2 DESTINATION day1)
install(FILES day1_input.txt DESTINATION input/)