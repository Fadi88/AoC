cmake_minimum_required(VERSION 3.8)

add_executable(day02 day02.cpp)


#install(TARGETS day02 DESTINATION ${CMAKE_CURRENT_BINARY_DIR}/day02)
install(FILES day02_input.txt DESTINATION ${CMAKE_CURRENT_BINARY_DIR}/input/)
