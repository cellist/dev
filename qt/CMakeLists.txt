#https://code.qt.io/cgit/qt/qtbase.git/tree/examples/qtconcurrent/wordcount?h=5.15

cmake_minimum_required(VERSION 3.13)

project(wordcount VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Qt5 COMPONENTS Concurrent REQUIRED)
add_executable(wordcount wordcount.cpp)
target_link_libraries(wordcount Qt5::Concurrent)
