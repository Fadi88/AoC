add_executable(dayxx dayxx.cpp)

install(TARGETS dayxx DESTINATION dayxx)
install(FILES dayxx_input.txt DESTINATION dayxx/input)