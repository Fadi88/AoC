cmake_minimum_required(VERSION 3.0)

add_executable(day2 day2.cpp)

install(TARGETS day2 DESTINATION day2)
install(FILES day2_input.txt DESTINATION day2/input)