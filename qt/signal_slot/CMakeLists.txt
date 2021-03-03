cmake_minimum_required(VERSION 3.13)

project(signal-slot VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

find_package(Qt5 COMPONENTS Core Widgets REQUIRED)

add_executable(signal-slot example.cpp)

target_link_libraries(signal-slot Qt5::Core)

add_executable(thread-example controller.cpp worker.cpp)

target_link_libraries(thread-example Qt5::Core)

add_executable(basic_thread basic_thread.cpp mythread.cpp)

target_link_libraries(basic_thread Qt5::Core)
