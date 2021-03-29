# https://github.com/shinnok/netcatgui/
cmake_minimum_required(VERSION 3.13)

project(clientsocketcomm VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

find_package(Qt5 COMPONENTS Core Network REQUIRED)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -g")

add_executable(clntcomm context.cpp main.cpp client.cpp getopt.cpp)

target_link_libraries(clntcomm Qt5::Core Qt5::Network)
