cmake_minimum_required(VERSION 3.1.0)

project(simple_socket)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

find_package(Qt5 COMPONENTS Network REQUIRED)

add_executable(
  simple_socket
  main.cpp
  mytcpsocket.cpp
  )

qt5_use_modules(simple_socket Network)

target_link_libraries(simple_socket Qt5::Network)
