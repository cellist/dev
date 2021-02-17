cmake_minimum_required(VERSION 2.4)

project(simple_logging)

add_executable(simple_logging demo.cpp)
target_link_libraries(simple_logging log4cplus)
