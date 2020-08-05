cmake_minimum_required(VERSION 3.8)

add_executable(day01 day01.cpp)


#install(TARGETS day01 DESTINATION ${CMAKE_CURRENT_BINARY_DIR}/day01)
install(FILES day01_input.txt DESTINATION ${CMAKE_CURRENT_BINARY_DIR}/input/)