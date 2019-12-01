cmake_minimum_required(VERSION 3.0)

add_executable(day1_task1 day1_task1.cpp)
add_executable(day1_task2 day1_task2.cpp)

install(TARGETS day1_task1 day1_task2 DESTINATION day1)
install(FILES day1_input.txt DESTINATION day1/input/)