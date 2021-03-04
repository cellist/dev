# https://code.qt.io/cgit/qt/qtbase.git/tree/examples/corelib/threads/mandelbrot?h=5.15
cmake_minimum_required(VERSION 3.13)

project(threaded-mandelbrot VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

find_package(Qt5 COMPONENTS Widgets REQUIRED)

add_executable(mandelbrot
  mandelbrotwidget.cpp
  renderthread.cpp
  main.cpp
)

target_link_libraries(mandelbrot Qt5::Widgets)
