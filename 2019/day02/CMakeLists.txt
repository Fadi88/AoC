cmake_minimum_required(VERSION 3.0)

add_executable(day02 day.cpp)

install(TARGETS day02 DESTINATION day02)
install(FILES input.txt DESTINATION day02/input)