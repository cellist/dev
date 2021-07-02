# https://qastack.com.de/programming/1120140/how-can-i-read-and-parse-csv-files-in-c
cmake_minimum_required(VERSION 2.4)

project(handle_csv)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -g")

add_executable(loadcsv loadcsv.cpp)

