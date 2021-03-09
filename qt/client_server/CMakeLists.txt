# https://stackoverflow.com/questions/20546750/qtcpsocket-reading-and-writing

cmake_minimum_required(VERSION 3.13)

project(client_server VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

find_package(Qt5 COMPONENTS Network REQUIRED)
add_executable(client_server main.cpp Client.cpp Server.cpp)
target_link_libraries(client_server Qt5::Network)
