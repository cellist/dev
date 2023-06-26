cmake_minimum_required(VERSION 3.12)
project(StdThreadsExample)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Add the executable target
add_executable(std-threads std-threads.cpp)

# Find and link the required threads library
find_package(Threads REQUIRED)
target_link_libraries(std-threads PRIVATE Threads::Threads)
