cmake_minimum_required(VERSION 3.10)

project(simple)

find_package(PostgreSQL REQUIRED)
include_directories (${PostgreSQL_INCLUDE_DIRS})
link_directories(${PostgreSQL_LIBRARY_DIRS})

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -lpqxx -lpq")

add_executable(simple simple.cxx)
add_executable(threads threads.cxx)

