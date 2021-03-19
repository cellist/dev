# https://studiofreya.com/cpp/boost/say-goodbye-to-memory-leaks-in-c-with-boost/
cmake_minimum_required(VERSION 2.4)

project(memory_leak_boost_lib)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -g")

add_executable(mem_leak mem_leak.cpp)

add_executable(no_leak no_leak.cpp)
