cmake_minimum_required(VERSION 3.1.0)

# Source:
# https://medium.com/@naveen.maltesh/generating-code-coverage-report-using-gnu-gcov-lcov-ee54a4de3f11

project(main_test VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Add code coverage compilation flags
set(CXX_COVERAGE_COMPILE_FLAGS "-fprofile-instr-generate -fcoverage-mapping")

set( CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} ${CXX_COVERAGE_COMPILE_FLAGS}" )

add_executable(main main.cpp)

add_executable(
  main_test
  main_test.cpp
)

target_link_libraries(main_test gtest pthread)
