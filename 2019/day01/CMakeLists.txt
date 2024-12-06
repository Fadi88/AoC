cmake_minimum_required(VERSION 3.0)

add_executable(day01 day.cpp)

install(TARGETS day01 DESTINATION day01)
install(FILES input.txt DESTINATION day01/input/)