cmake_minimum_required(VERSION 2.4)

project(memoryLeak)

set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -g -Og")

add_executable(memoryLeak memoryLeak.c)
