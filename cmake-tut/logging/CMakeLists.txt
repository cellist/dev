cmake_minimum_required(VERSION 2.4)

project(logging)

add_executable(simple_logging demo.cpp)
target_link_libraries(simple_logging log4cplus)

add_executable(advanced_logging advanced.cpp)
target_link_libraries(advanced_logging log4cplus)
