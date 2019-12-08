cmake_minimum_required(VERSION 3.0)

add_executable(day1 day1.cpp)


install(TARGETS day1 DESTINATION day1)
install(FILES day1_input.txt DESTINATION day1/input/)